from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json

import os
import time
import psycopg2
import json
from psycopg2.extras import Json

PUBSUB_PROJECT_ID = os.environ.get("PUBSUB_PROJECT_ID")
PUBSUB_SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
PUBSUB_TIMEOUT = int(os.environ.get("PUBSUB_TIMEOUT", 900))
PUBSUB_MAX_MESSAGES = int(os.environ.get("PUBSUB_MAX_MESSAGES", 100))

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")


# Parse the connection string
DB_PARAMS = psycopg2.extensions.make_dsn(DB_CONNECTION_STRING)

SQL_QUERY = """
       call insert_event_procedure(%s, %s, %s::timestamp with time zone, %s, %s::jsonb[], %s::jsonb[]);
    """

def extract(project_id, subscription_id, timeout=10, max_messages=10):
    """Receives messages from a pull subscription with flow control."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data!r}.")
        message.ack()

        message_data = message.data.decode("utf-8")
        message_json = dict()
        try:
            message_json = json.loads(message_data)
        except json.JSONDecodeError as e:
            pass # Drop the message if it is not a valid json string

        with psycopg2.connect(DB_PARAMS) as conn:
          with conn.cursor() as cur:
            cur.execute(SQL_QUERY, (message_json.get('lg_id'),
                                  message_json.get('en_id'),
                                  message_json.get('ev_ts'),
                                  message_json.get('aw_id'),
                                  [Json(item) for item in message_json.get('dims', [])],
                                  [Json(item) for item in message_json.get('metrics', [])]))


    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=max_messages)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, 
        callback=callback, 
        await_callbacks_on_shutdown=True, 
        flow_control=flow_control
    )

    print(f"Listening for messages on {subscription_path}..\n")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


while True:
  extract(PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID, PUBSUB_TIMEOUT, PUBSUB_MAX_MESSAGES)
  time.sleep(1)
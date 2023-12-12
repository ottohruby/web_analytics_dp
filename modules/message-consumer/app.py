from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json

import os
import time
import psycopg2
import json
from psycopg2.extras import Json
from psycopg2.pool import ThreadedConnectionPool

PUBSUB_PROJECT_ID = os.environ.get("PUBSUB_PROJECT_ID")
PUBSUB_SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
PUBSUB_TIMEOUT = int(os.environ.get("PUBSUB_TIMEOUT", 900))
PUBSUB_MAX_MESSAGES = int(os.environ.get("PUBSUB_MAX_MESSAGES", 100))

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")


# Parse the connection string
DB_PARAMS = psycopg2.extensions.make_dsn(DB_CONNECTION_STRING)

SQL_QUERY = """
       select insert_event_data(%s, %s, %s::timestamp with time zone, %s, %s::jsonb[], %s::jsonb[]);
    """

db_connection_pool = ThreadedConnectionPool(minconn=10, maxconn=10, dsn=DB_PARAMS)

def handle_message(message):
    message_json = dict()
    try:
        message_json = json.loads(message)
    except json.JSONDecodeError as e:
        pass  # Drop the message if it is not a valid JSON string

    with db_connection_pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                SQL_QUERY,
                (
                    message_json.get('lg_id'),
                    message_json.get('en_id'),
                    message_json.get('ev_ts'),
                    message_json.get('aw_id'),
                    [Json(item) for item in message_json.get('dims', [])],
                    [Json(item) for item in message_json.get('metrics', [])]
                )
            )
    db_connection_pool.putconn(conn)

def extract(project_id, subscription_id, timeout=10, max_messages=10):
    """Receives messages from a pull subscription with flow control."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        # print(f"Received {message.data!r}.")
        message.ack()

        message_data = message.data.decode("utf-8")
        handle_message(message_data)


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

sa = {
  "type": "service_account",
  "project_id": "otto-hruby-dp",
  "private_key_id": "24786b0f7c458b9cbaacc4ef6f74677e775b9c2a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3V+sigKflENJh\nxxk1qyfdwp2pvRvbyjdCQ4GRvjtq7Gguj/47sFvZlmGyMqonXqdG0+j4Ca9ATAzt\ncF38rNqAiI9UR5GznE4umoiB1x4z9g0WBpmYiBg88bCZSvJidIc7jmyEYSdmdXKq\nDyetf2+nwPgH2YlA+dZ/izqz1oEN+UDdG5rDOXQOhXK74ECFTEFftKvgEEYnjKkB\ncJYE2U2PDtc/FAkrMIk7xeG/V5kGbVbGeLW33BK2wr1nuUcpRQV3SGEZkT0lETAQ\nObQ9RBl7B/jWLulX60uLw0RqnLPd7x2NwdAtBReu4LO2cD/k6pkRXlzaNEWX1ko0\n7mLW2qtVAgMBAAECggEAGOmIWKrUpWpwu7p68XDtPNO56pt4kpfahFV54JzRpAi1\na0ZDjEa9ZEZrxfPebPUOk7Atoq5mMr1isEypaLDwC7ECkLgc0yP0954l2EarovHW\n+1wwOKqdaIKKtXmaj8g3q98BXcd5vBFPYE4o3QlI2al9yktDvCF2hOQdONx3srcl\nYTQjTRPN7QOYjeFLF0Ra5tlP+IVDovzYLRsvkYw5Xs/PCITkjzDdtHae7qXfF2J/\nCWl/ySsR+APIjz/3Um8ywn3k0VYjFbvvwaTLLHR0cq8ZltaLcY4KzHo96+qrzOlB\nM4HAsMcBxYa6mGQVTF/RPOyc4D/lqjMhpsLxJiyKLQKBgQDxd5ncjXkpqhJlQOI+\nY3elrqrafmFSJmev1EbLIlVBd05UbAEo+lZu/uizngrAUWn2xAh+pX9MHxrtW7++\nAKvtBCOsEUNy6YMrY1Tx7/LYcTtoFKZqp0tQ+ISHQkLDCGs5/wcqrME0l4Fqd/DB\nogk80QOgGTDqLFF4YsDjQPtkswKBgQDCYMb7b9GgH7K93SRUgewBDP8oWUhC2krN\nBWT+aKF1bI2aXA9AUkYGa8VsTdYYsUmuJiC4tJ6iG9/MDMO7Zf0TOgCl/ZxnQeDx\nHDCLL2bJ/T/O0xDH0lxpPVhe3CcB83gKof3TG9QoL5eg5JzTMrh984tbEpPRV1Ce\nIqefO8kD1wKBgHhoU2kPguOr0xB6klbZ8sfDmZ7qdk0oqXucNtEEhc7nVz/xu4Jb\nks42foNSw7my30wV5MaCcD/dIuhJYAu2+gRuk/sxgJjEqIvyNGGQbWBQ1nbIFVQJ\nqBzwT+XCvNfUUuPQsBovmwhGpFobBQsJaeHRuCUVarba8qU9WUH5HWLRAoGBAJa/\nzbK1TyNbUhmUB5gOxwUtmjolvDg06ixFUcVJSmcyUEP1v9JHvI1ASfWsDC5MWPNa\nGKiHVDwvWAr9n1OYToT5yAT0QreGTTlRfoiDs7lV0oXKBcqjaA4qiH3RSeNmeqPs\nbFmszIZ6GqOqicH2JUVxe5OfPcruZ9Ss1clV6ZkzAoGANflmB0E/bZlolbB45ww0\ntgFcHCCcCxl57abMpwS0UuJdEh2qLPCBpoLaOjtP+WWDdd7lGTz0Ma47lkSTZnJG\nAe2ZnQIsU5stsKWkm4GXVREKFUq1CQOpEkzWpVH8C3CXrZDGUd1KJp2MtLFJMBV2\njRuE1Nk4nYf3guPQV+rGCe8=\n-----END PRIVATE KEY-----\n",
  "client_email": "debugging@otto-hruby-dp.iam.gserviceaccount.com",
  "client_id": "104928544285908817979",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/debugging%40otto-hruby-dp.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Write the dictionary to a JSON file
with open("secrets.json", "w") as json_file:
    json.dump(sa, json_file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets.json"
while True:
  extract(PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID, PUBSUB_TIMEOUT, PUBSUB_MAX_MESSAGES)
  time.sleep(1)
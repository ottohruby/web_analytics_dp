from google.cloud import pubsub_v1
import json

from src.config import PubsubConfig

batch_settings = pubsub_v1.types.BatchSettings(
        max_messages = PubsubConfig.MAX_MESSAGES,
        max_bytes = PubsubConfig.MAX_BYTES,
        max_latency = PubsubConfig.MAX_LATENCY,
)
publisher = pubsub_v1.PublisherClient(batch_settings)
topic_path = publisher.topic_path(PubsubConfig.PROJECT_ID, PubsubConfig.TOPID_ID)

def publish_to_pubsub(json_data):
    byte_string = json.dumps(json_data).encode('utf-8')
    publisher.publish(topic_path, byte_string)

data "google_project" "project" {
    project_id= var.project_id
}

variable "schema-data-logger-events" {
  description = "Protocol Buffers schema definition"
  type        = string
  default = <<EOF
syntax = "proto3";

message Item {
    string category = 1;
    string id = 2;
    string list = 3;
    string name = 4;
    string position = 5;
    string quantity = 6;
    string unit = 7;
    string value = 8;
}

message Event {
    string event_date = 1;
    string event_timestamp_micros = 2;
    string event_name = 3;
    string description = 4;
    string device_id = 5;
    string device_type = 6;
    string is_conversion = 7;
    string is_new_device = 8;
    string is_new_session = 9;
    string items_quantity = 10;
    repeated Item items = 11;
    string event_value = 12;
    string event_unit = 13;
    string event_source = 14;
    string event_medium = 15;
    string event_campaign = 16;
    string privacy = 17;
    string session_campaign = 18;
    string session_id = 19;
    string session_medium = 20;
    int32 session_number = 21;
    string session_source = 22;
    string user_agent = 23;
}
EOF
}


resource "google_pubsub_schema" "data-logger-events" {
  name = "data-logger-events"
  type = "PROTOCOL_BUFFER"
  definition = var.schema-data-logger-events
}

resource "google_pubsub_topic" "data-logger-events" {
  project = var.project_id
  name = "data-logger-events"

  depends_on = [google_pubsub_schema.data-logger-events]
  schema_settings {
    schema = "projects/${var.project_id}/schemas/${google_pubsub_schema.data-logger-events.name}"
    encoding = "JSON"
  }

}

resource "google_pubsub_topic_iam_binding" "binding" {
  project = var.project_id
  topic = google_pubsub_topic.data-logger-events.name
  role = "roles/pubsub.publisher"

  members = [
    "allUsers"
  ]

  depends_on = [
    google_pubsub_topic.data-logger-events
  ]
}

resource "google_pubsub_subscription" "data-logger-events--pull--realtime" {
  project = var.project_id
  name  = "data-logger-events--pull--realtime"
  topic = google_pubsub_topic.data-logger-events.name

  message_retention_duration = "1800s" # 30 minutes
  ack_deadline_seconds = 20
  enable_message_ordering = false
}

resource "google_pubsub_subscription" "data-logger-events--bigquery--all" {
  project = var.project_id
  name  = "data-logger-events--bigquery--all"
  topic = google_pubsub_topic.data-logger-events.name

  bigquery_config {
    table = "${google_bigquery_table.data_logger_events.project}.${google_bigquery_table.data_logger_events.dataset_id}.${google_bigquery_table.data_logger_events.table_id}"
  }

  depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}

resource "google_project_iam_member" "viewer" {
  project = var.project_id
  role   = "roles/bigquery.metadataViewer"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "editor" {
  project = data.google_project.project.project_id
  role   = "roles/bigquery.dataEditor"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_bigquery_dataset" "data_logger" {
  project = var.project_id
  dataset_id = "data_logger"
}

resource "google_bigquery_table" "data_logger_events" {
  project = var.project_id
  deletion_protection = false
  table_id   = "events"
  dataset_id = google_bigquery_dataset.data_logger.dataset_id

  schema = <<EOF
[
  {
    "name": "data",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The data"
  }
]
EOF
}









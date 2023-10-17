data "google_project" "project" {
    project_id= var.project_id
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
    use_topic_schema = true
    drop_unknown_fields = true
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

  schema = var.schema-bq-data_logger_events
}









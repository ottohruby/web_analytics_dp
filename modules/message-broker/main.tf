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


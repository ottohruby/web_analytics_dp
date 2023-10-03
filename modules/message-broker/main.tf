resource "google_pubsub_topic" "data-logger-events" {
  project = var.project_id
  name = "data-logger-events"
}
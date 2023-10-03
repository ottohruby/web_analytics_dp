
resource "google_service_account" "service_account" {
  account_id   = "run-service--data-logger"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = "${var.project_id}"
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}
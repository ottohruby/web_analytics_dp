

resource "google_service_account" "service_account" {
  account_id   = "run-service--data-logger"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_cloud_run_v2_service" "data-logger" {
  project = var.project_id
  location = var.region
  name = "data-logger"

  template {
    service_account = google_service_account.service_account.email
    containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/data-logger/data-logger:latest"

        env {
            name = "PUBSUB_PROJECT_ID"
            value = "${var.project_id}"
        }
    }
  }
}

resource "google_cloud_run_domain_mapping" "data-logger" {
  count = var.data-logger_domain != "" ? 1 : 0
  project = var.project_id
  location = var.region
  name     = var.data-logger_domain

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_v2_service.data-logger.name
  }
}

resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloud_run_v2_service.data-logger.location
  service  = google_cloud_run_v2_service.data-logger.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

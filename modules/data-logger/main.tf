
resource "google_service_account" "service_account" {
  account_id   = "run-service--data-logger"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = "${var.project_id}"
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_cloud_run_v2_service" "data-logger" {
  name     = "data-logger"
  location = var.project_id

  template {
    service_account = google_service_account.service_account.email
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }
}

resource "google_cloud_run_domain_mapping" "data-logger" {
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
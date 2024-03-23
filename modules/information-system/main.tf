data "google_project" "project" {
}

resource "google_compute_instance" "information-system" {
  boot_disk {
    auto_delete = true
    device_name = "information-system"

    initialize_params {
      image = "projects/cos-cloud/global/images/cos-stable-109-17800-66-27"
      size  = 10
      type  = "pd-standard"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    container-vm = "cos-stable-109-17800-66-27"
    goog-ec-src  = "vm_add-tf"
  }

  machine_type = "e2-micro"

  metadata = {
    gce-container-declaration = "spec:\n  containers:\n  - name: information-system\n    image: ${var.region}-docker.pkg.dev/${var.project_id}/information-system/information-system:latest\n    env:\n    - name: PUBSUB_PROJECT_ID\n      value: ${var.project_id}\n    - name: PUBSUB_SUBSCRIPTION_ID\n      value: data-logger-events--pull--realtime\n    - name: SQLALCHEMY_DATABASE_URI\n      value: postgresql://${var.db_user}:${var.db_password}@${var.sql_ip}/postgres\n    stdin: false\n    tty: false\n  restartPolicy: Always\n# This container declaration format is not public API and may change without notice. Please\n# use gcloud command-line tool or Google Cloud Console to run Containers on Google Compute Engine."
  }

  name = "information-system"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    subnetwork = "projects/${var.project_id}/regions/${var.region}/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  zone = "${var.region}-b"
}

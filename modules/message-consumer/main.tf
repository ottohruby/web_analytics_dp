# This code is compatible with Terraform 4.25.0 and versions that are backward compatible to 4.25.0.
# For information about validating this Terraform code, see https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration

resource "google_compute_instance" "instance-6" {
  boot_disk {
    auto_delete = true
    device_name = "instance-3"

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
    gce-container-declaration = "spec:\n  containers:\n  - name: instance-6\n    image: europe-west1-docker.pkg.dev/otto-hruby-dp/message-consumer/message-consumer@sha256:28f703a64eb31a4529caa278e0a4c2e5293c18ffbbe46e73c207fc0f032c29c4\n    env:\n    - name: PUBSUB_PROJECT_ID\n      value: otto-hruby-dp\n    - name: PUBSUB_SUBSCRIPTION_ID\n      value: data-logger-events--pull--realtime\n    - name: DB_CONNECTION_STRING\n      value: postgresql://postgres:postgres@35.187.7.142/postgres\n    stdin: false\n    tty: false\n  restartPolicy: Always\n# This container declaration format is not public API and may change without notice. Please\n# use gcloud command-line tool or Google Cloud Console to run Containers on Google Compute Engine."
  }

  name = "instance-6"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    subnetwork = "projects/otto-hruby-dp/regions/europe-west1/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "280193624624-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  zone = "europe-west1-b"
}

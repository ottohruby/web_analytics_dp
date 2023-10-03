provider "google" {
  project = "${var.project_id}"
  region = "${var.region}"
}

variable "gcp_required_apis"{
  type = list(string)
  default= [
    "cloudresourcemanager.googleapis.com",
    "apikeys.googleapis.com",
    "compute.googleapis.com",
    "sqladmin.googleapis.com",
    "iam.googleapis.com"
    ]
}

resource "google_project_service" "gcp_api" {
  for_each = toset(var.gcp_required_apis)
  project = var.project_id
  service = each.key
}

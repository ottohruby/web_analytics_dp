provider "google" {
    project = "${var.project_id}"
    region = "${var.region}"
}

variable "required_apis"{
    type = list(string)
    default= [
        "cloudresourcemanager.googleapis.com",
        "apikeys.googleapis.com",
        "compute.googleapis.com",
        "sqladmin.googleapis.com",
        "iam.googleapis.com"
    ]
}

resource "google_project_service" "api" {
    for_each = toset(var.required_apis)
    project = var.project_id
    service = each.key
}

module "data-logger" {
    source = "./modules/data-logger"
    depends_on = [google_project_service.api]

    project_id = var.project_id
    region = var.region
    data-logger_domain = var.data-logger_domain
}

module "message-broker" {
    source = "./modules/message-broker"

    project_id = var.project_id
    region = var.region 
}


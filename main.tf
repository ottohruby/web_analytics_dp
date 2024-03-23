terraform {
  required_providers {
    google = "~> 5.1.0"
  }
}

provider "google" {
    project = var.project_id
    region = var.region
}

resource "google_project_service" "cloud_serviceusage_api" {
  project                    = var.project_id
  service                    = "serviceusage.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "cloudresourcemanager_api" {
  depends_on                 = [google_project_service.cloud_serviceusage_api]
  project                    = var.project_id
  service                    = "cloudresourcemanager.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "api" {
    depends_on = [google_project_service.cloudresourcemanager_api]
    for_each = toset(var.required_apis)
    project = var.project_id
    service = each.key
    disable_dependent_services = true
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
    depends_on = [google_project_service.api]

    project_id = var.project_id
    region = var.region 
}

module "postgresql" {
  source = "./modules/postgresql"
  depends_on = [google_project_service.api]

  project_id = var.project_id
  region = var.region
  db_password = var.db_password
}

module "message-consumer" {
    source = "./modules/message-consumer"
    depends_on = [google_project_service.api, module.postgresql
    ]

    project_id = var.project_id
    region = var.region
    sql_ip = module.postgresql.public_ip_address
    db_user = module.postgresql.db_user
    db_password = module.postgresql.db_password

}

module "information-system" {
    source = "./modules/information-system"
    depends_on = [google_project_service.api, module.postgresql
    ]

    project_id = var.project_id
    region = var.region
    sql_ip = module.postgresql.public_ip_address
    db_user = module.postgresql.db_user
    db_password = module.postgresql.db_password

}

variable "project_id" {
    type = string
}

variable "region" {
    type = string
    default = "europe-west1"
}

variable "data-logger_domain"{
    type = string
    default = ""
}

variable "db_password"{
    type = string
}

variable "required_apis"{
    type = list(string)
    default= [
        "apikeys.googleapis.com",
        "compute.googleapis.com",
        "sqladmin.googleapis.com",
        "iam.googleapis.com",
        "pubsub.googleapis.com",
        "run.googleapis.com"
    ]
}


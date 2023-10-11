variable "project_id" {
    type = string
    default = "otto-hruby-dp"
}
variable "region" {
    type = string
    default = "europe-west1"
}

variable "data-logger_domain"{
    type = string
    default = "dp-logger.ottohruby.cz"
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


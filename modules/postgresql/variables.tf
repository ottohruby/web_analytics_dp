variable "project_id" {
    type = string
}

variable "region" {
    type = string
}

variable "db_user"{
    type = string
    default = "admin_user"
}

variable "db_password"{
    type=string
    sensitive = true
}


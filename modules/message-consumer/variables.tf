variable "project_id" {
    type = string
}

variable "region" {
    type = string
}

variable "sql_ip"{
    type = string
}

variable "db_user"{
    type = string
}

variable "db_password"{
    type=string
    sensitive = true
}

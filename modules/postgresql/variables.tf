variable "project_id" {
    type = string
}

variable "region" {
    type = string
}

variable "db_credentials" {
  type = object({
    db_user    = string
    db_password = string
  })
  
  default = {
    db_user = "admin_user"
    db_password = "admin_user123" 
  }

  sensitive = true
}

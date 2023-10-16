resource "google_sql_database_instance" "main" {
    project = var.project_id
    region = var.region

    name = "main-instance"
    database_version = "POSTGRES_15"
  
  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro" # 0.6 GB RAM, 1 Shared CPU ~ 8 USD / mo
    edition = "ENTERPRISE"
    availability_type = "ZONAL"

    disk_autoresize = true
    disk_autoresize_limit = 50
    disk_size = 10
    disk_type = "PD_SSD"
    database_flags {
      name = "cloudsql.enable_pg_cron"
      value = "On"
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        value = "0.0.0.0/0" # All ips, for development
        name = "all"
      }
    }
  }
}

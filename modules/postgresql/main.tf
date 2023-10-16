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

// DATABASE USER
resource "google_sql_user" "user" {
    instance = google_sql_database_instance.main.name

    name     = var.db_credentials.db_user
    password = var.db_credentials.db_password

    depends_on = [
        google_sql_database_instance.main
    ]

    provisioner "local-exec" {
        command = "psql postgresql://${google_sql_user.user.name}:${google_sql_user.user.password}@${google_sql_database_instance.main.public_ip_address}/postgres -f db_init.sql"
    }
}

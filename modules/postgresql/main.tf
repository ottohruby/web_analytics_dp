resource "google_sql_database_instance" "main" {
    project = var.project_id
    region = var.region

    name = "main-instance"
    database_version = "POSTGRES_15"
  
  settings {
    tier = "db-g1-small" # 1.7 GB RAM, 1 Shared CPU
    edition = "ENTERPRISE"
    availability_type = "ZONAL"

    disk_autoresize = true
    disk_autoresize_limit = 100
    disk_size = 10
    disk_type = "PD_SSD"
    database_flags {
      name = "cloudsql.enable_pg_cron"
      value = "On"
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        value = "0.0.0.0/0"
        name = "all"
      }
    }
  }
}

resource "google_sql_user" "root_user" {
    instance = google_sql_database_instance.main.name
    name     = "postgres"
    password = var.db_password

    depends_on = [
        google_sql_database_instance.main
    ]
}

// DATABASE USER
resource "google_sql_user" "user" {
    instance = google_sql_database_instance.main.name

    name     = var.db_user
    password = var.db_password

    depends_on = [
        google_sql_database_instance.main
    ]

    provisioner "local-exec" {
        command = <<EOF
            psql postgresql://${var.db_user}:${var.db_password}@${google_sql_database_instance.main.public_ip_address}/postgres <<EOS 
                CREATE EXTENSION pg_cron;
                CREATE SCHEMA analytics;
                $(cat ${path.module}/tables/0_states.sql)

                $(cat ${path.module}/tables/1_agg_windows.sql)
                $(cat ${path.module}/tables/1_event_names.sql)
                $(cat ${path.module}/tables/1_loggers.sql)

                $(cat ${path.module}/tables/2_dimensions.sql)
                $(cat ${path.module}/tables/2_event_stats.sql)
                $(cat ${path.module}/tables/2_metric_functions.sql)
                $(cat ${path.module}/tables/2_modules.sql)
                $(cat ${path.module}/tables/2_roles.sql)
                $(cat ${path.module}/tables/2_units.sql)
                $(cat ${path.module}/tables/2_metrics.sql)
                $(cat ${path.module}/tables/2_users.sql)
                $(cat ${path.module}/tables/2_reports.sql)

                $(cat ${path.module}/tables/3_allowed_event_dimensions.sql)
                $(cat ${path.module}/tables/3_allowed_event_metrics.sql)
                $(cat ${path.module}/tables/3_event_dimensions.sql)
                $(cat ${path.module}/tables/3_event_metrics.sql)
                $(cat ${path.module}/tables/3_module_roles.sql)
                $(cat ${path.module}/tables/3_user_roles.sql)

                $(cat ${path.module}/functions/insert_event_data.sql)
                $(cat ${path.module}/functions/get_event_data.sql)
                $(cat ${path.module}/functions/process_event_data.sql)
                $(cat ${path.module}/functions/cron.sql)
            EOS
        EOF
    }
}

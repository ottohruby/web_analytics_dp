output "public_ip_address" {
  description = "The public IPv4 address of the master instance."
  value       = google_sql_database_instance.main.public_ip_address
}

output "db_user" {
  value       = google_sql_user.user.name
}

output "db_password" {
  value       = google_sql_user.user.password
}



variable "project_id" {
    type = string
}

variable "region" {
    type = string
}


variable "schema-data-logger-events" {
  description = "Protocol Buffers schema definition"
  type        = string
  default = <<EOF
syntax = "proto3";

message Event {
    message Dimension {
   	    int64 id = 1;
   	    string val = 2;
    }

    message Metric {
   	    int64 id = 1;
   	    string val = 2;
   	    int64 unit = 3;
    }

   	string ev_ts = 1;
   	int64 en_id = 2;
   	int64 lg_id = 3;
    int64 aw_id = 4;
   	repeated Dimension dims = 5;
   	repeated Metric metrics = 6;
}

EOF
}

variable "schema-bq-data_logger_events" {
    description = "Bigquery schema definition"
    type        = string
    default     = <<EOF
[
    {
        "name": "event_date",
        "type": "DATE",
        "description": "The date when the event occurred."
    },
    {
        "name": "event_timestamp_micros",
        "type": "INTEGER",
        "description": "The timestamp in microseconds when the event occurred."
    },
    {
        "name": "event_name",
        "type": "STRING",
        "description": "The name of the event."
    },
    {
        "name": "page_domain",
        "type": "STRING",
        "description": "The domain or website where the page event occurred."
    },
    {
        "name": "page_path",
        "type": "STRING",
        "description": "The path or URL of the page where the event took place."
    },
    {
        "name": "page_title",
        "type": "STRING",
        "description": "The title of the page where the event occurred."
    },
    {
        "name": "device_id",
        "type": "STRING",
        "description": "The unique identifier for the device."
    },
    {
        "name": "device_type",
        "type": "STRING",
        "description": "The type of the device."
    },
    {
        "name": "event_value",
        "type": "NUMERIC",
        "description": "The value associated with the event."
    },
    {
        "name": "event_unit",
        "type": "STRING",
        "description": "The unit of measurement for the event value."
    },
    {
        "name": "session_source",
        "type": "STRING",
        "description": "The source of the session."
    },
    {
        "name": "session_medium",
        "type": "STRING",
        "description": "The medium of the session."
    },
    {
        "name": "session_campaign",
        "type": "STRING",
        "description": "The campaign associated with the session."
    },
    {
        "name": "session_id",
        "type": "STRING",
        "description": "The unique identifier for the session."
    },
    {
        "name": "session_number",
        "type": "INTEGER",
        "description": "The session number."
    },
    {
        "name": "user_agent",
        "type": "STRING",
        "description": "The user agent information for the event."
    },
    {
        "name": "items_quantity",
        "type": "INTEGER",
        "description": "The quantity of items associated with the event."
    },
    {
        "name": "items",
        "type": "RECORD",
        "mode": "REPEATED",
        "fields": [
            {
                "name": "category",
                "type": "STRING",
                "description": "The category of the item."
            },
            {
                "name": "id",
                "type": "STRING",
                "description": "The unique identifier of the item."
            },
            {
                "name": "list",
                "type": "STRING",
                "description": "The list or group to which the item belongs."
            },
            {
                "name": "name",
                "type": "STRING",
                "description": "The name or title of the item."
            },
            {
                "name": "position",
                "type": "INTEGER",
                "description": "The position of the item in the list."
            },
            {
                "name": "quantity",
                "type": "INTEGER",
                "description": "The quantity of the item."
            },
            {
                "name": "unit",
                "type": "STRING",
                "description": "The unit of measurement for the item."
            },
            {
                "name": "value",
                "type": "NUMERIC",
                "description": "The value or price of the item."
            }
        ]
    }
]

EOF
}
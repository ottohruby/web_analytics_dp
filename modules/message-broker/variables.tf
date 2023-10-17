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
    string event_date = 1;
    int64 event_timestamp_micros = 2;
    string event_name = 3;

    string page_domain = 4;
    string page_path = 5;
    string page_title = 6;

    string user_agent = 7;

    string device_id = 8;
    string device_type = 9;

    int32 is_conversion = 10;
    
    string event_value = 11;
    string event_unit = 12;

    string session_source = 13;
    string session_medium = 14;
    string session_campaign = 15;

    string session_id = 16;
    int32 session_number = 17;
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
        "name": "is_conversion",
        "type": "INTEGER",
        "description": "A flag indicating if the event is a conversion event (1 means conversion)."
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
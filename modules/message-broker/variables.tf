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


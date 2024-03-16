DROP TABLE IF EXISTS analytics.event_stats CASCADE;

CREATE TABLE analytics.event_stats (
    event_id serial PRIMARY KEY,
    lg_id int not null REFERENCES analytics.loggers(id),
    en_id int not null REFERENCES analytics.event_names(id),
    insertion_ts timestamp with time zone default current_timestamp,
    ev_ts timestamp with time zone default current_timestamp,
    aw_id int not null REFERENCES analytics.agg_windows(id),
    is_processed int default 0
);


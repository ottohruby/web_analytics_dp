DROP TABLE IF EXISTS analytics.event_stats CASCADE;
CREATE TABLE analytics.event_stats (
    event_id serial PRIMARY KEY,
    lg_id integer REFERENCES analytics.loggers(id),
    en_id integer REFERENCES analytics.event_names(id),
    ev_ts timestamp with time zone not null,
    insertion_ts timestamp with time zone default current_timestamp not null,
    aw_id integer REFERENCES analytics.agg_windows(id),
    is_processed integer not null default(0)
);
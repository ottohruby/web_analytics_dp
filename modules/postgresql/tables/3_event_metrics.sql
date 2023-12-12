DROP TABLE IF EXISTS analytics.event_metrics CASCADE;
CREATE TABLE analytics.event_metrics (
    id serial PRIMARY KEY,
    event_id integer REFERENCES analytics.event_stats(event_id),
    metric_id integer REFERENCES analytics.metrics(id),
    unit_id integer REFERENCES analytics.units(id),
    value numeric not null
);
DROP TABLE IF EXISTS analytics.event_metrics CASCADE;
CREATE TABLE analytics.event_metrics (
    id serial PRIMARY KEY,
    event_id integer REFERENCES analytics.event_stats(event_id) ON DELETE CASCADE,
    metric_id integer REFERENCES analytics.metrics(id),
    unit_id integer REFERENCES analytics.units(id),
    function_id integer REFERENCES analytics.metric_functions(id),
    value numeric default 0
);

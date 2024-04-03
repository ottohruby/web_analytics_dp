DROP TABLE IF EXISTS analytics.event_dimensions CASCADE;
CREATE TABLE analytics.event_dimensions (
    id serial PRIMARY KEY,
    event_id integer REFERENCES analytics.event_stats(event_id) ON DELETE CASCADE,
    dim_id integer REFERENCES analytics.dimensions(id),
    value varchar
);

DROP TABLE IF EXISTS analytics.event_names CASCADE;
CREATE TABLE analytics.event_names (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar
);
INSERT INTO analytics.event_names (event_name_id, event_name)
VALUES 
    (0, 'new_visitor'),
    (1, 'new_session'),
    (2, 'page_view'),
    (3, 'scroll'),
    (4, 'link_click'),
    (5, 'purchase'),
    (6, 'view_item_detail'),
    (7, 'purchase_item'),
    (8, 'add_item_to_cart')
    ;

DROP TABLE IF EXISTS analytics.event_stats CASCADE;
CREATE TABLE analytics.event_stats (
    event_id serial PRIMARY KEY,
    lg_id integer not null,
    en_id integer REFERENCES analytics.event_names(id),
    ev_ts timestamp with time zone not null,
    insertion_ts timestamp with time zone default current_timestamp not null,
    aw_id integer
);

-- Create the event_dimensions table
CREATE TABLE analytics.event_dimensions (
    dim_id integer,  -- You may want to define a foreign key constraint here
    event_id integer REFERENCES analytics.event_stats(event_id),
    value varchar
);

-- Create the event_metrics table
CREATE TABLE analytics.event_metrics (
    metric_id integer,  -- You may want to define a foreign key constraint here
    unit_id integer,    -- You may want to define a foreign key constraint here
    event_id integer REFERENCES analytics.event_stats(event_id),
    value numeric
);
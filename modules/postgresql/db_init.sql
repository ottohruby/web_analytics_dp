SELECT cron.schedule('realtime-delete-old', '* * * * *', $$DELETE FROM event_stats WHERE is_realtime = 1 and event_timestamp < now() - interval '2 day'$$);

DROP TABLE IF EXISTS state_transitions CASCADE;
CREATE TABLE state_transitions (
    id serial PRIMARY KEY,
    state_current INTEGER REFERENCES states (state_id),
    state_next INTEGER REFERENCES states (state_id),
    description varchar
);


DROP TABLE IF EXISTS states CASCADE;
CREATE TABLE states (
    state_id serial PRIMARY KEY,
    state_number INTEGER NOT NULL,
    description varchar,
    last_change timestamp
);


DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE states (
    user_id serial PRIMARY KEY,
    state_id INTEGER REFERENCES states (state_id),
    name VARCHAR NOT NULL,
    email VARCHAR,
    password_hash VARCHAR NOT NULL,
    login_failed_attempts INTEGER DEFAULT 0
);








DROP TABLE IF EXISTS modules CASCADE;
CREATE TABLE modules (
    module_id serial PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
);

DROP TABLE IF EXISTS forms CASCADE;
CREATE TABLE forms (
	form_id serial PRIMARY KEY,
    module_id INTEGER REFERENCES modules (module_id),
    name VARCHAR NOT NULL,
    description VARCHAR
);

DROP TABLE IF EXISTS form_items CASCADE;
CREATE TABLE form_items (
	form_item_id serial PRIMARY KEY,
    form_id INTEGER REFERENCES forms (form_id),
    key VARCHAR NOT NULL,
    value VARCHAR NOT NULL
);



DROP TABLE IF EXISTS AGG_WINDOWS CASCADE;
CREATE TABLE AGG_WINDOWS (
    agg_window_id serial PRIMARY KEY,
    name VARCHAR
);

INSERT INTO agg_windows (agg_window_id, name)
VALUES 
(0, 'REALTIME'),
(1, 'MINUTE'),
(2, 'HOUR'),
(3, 'DAY'),
(4, 'MONTH');

DROP TABLE IF EXISTS EVENT_NAMES CASCADE;
CREATE TABLE EVENT_NAMES (
    event_name_id serial PRIMARY KEY,
    event_name VARCHAR NOT NULL,
    description VARCHAR
);

INSERT INTO EVENT_NAMES (event_name_id, event_name)
VALUES 
    (0, 'new_device'),
    (1, 'new_session'),
    (2, 'page_view'),
    (3, 'scroll'),
    (4, 'click'),
    (5, 'time_on_page'),
    (6, 'link_click')
    ;

DROP TABLE IF EXISTS EVENT_STATS CASCADE;
CREATE TABLE EVENT_STATS (
	event_id serial PRIMARY KEY,
    event_name_id INTEGER REFERENCES EVENT_NAMES (event_name_id),
    agg_window_id INTEGER REFERENCES AGG_WINDOWS (agg_window_id),

    insertion_ts timestamp with time zone default NOW(),
    event_ts INTEGER
);

drop table if EXISTS metrics;
create table metrics (
    metric_id serial primary key,
    metric_code varchar,
    metric_name varchar,
    is_base integer,
    description varchar
);

INSERT INTO metrics (metric_id, metric_code)
VALUES 
    (0, 'event_count'),
    (1, 'percent'),
    (2, 'value'),
    (3, 'quantity'),
    (4, 'price'),
    (5, 'position'),
    (6, 'time');

DROP TABLE IF EXISTS EVENT_METRICS CASCADE;
CREATE TABLE EVENT_METRICS (
    id serial PRIMARY KEY,
    metric_id integer REFERENCES metrics (metric_id),
    event_id integer REFERENCES event_stats (event_id),
    value numeric not null
);


drop table if EXISTS dimensions;
create table dimensions (
    dim_id serial primary key,
    dim_name varchar,
    description varchar
);

drop table if EXISTS event_dimensions;
create table event_dimensions (
    id serial primary key,
    dim_id integer REFERENCES dimensions(dim_id),
    event_id integer REFERENCES event_stats(event_id),
    value varchar
);



-- with events (agg_window_id, event_name, batch_seq_id) AS
-- (
--     VALUES
--     (0, 'page_view', 1),
--     (0, 'scroll', 2)
-- ),
-- metrics (metric_code, value, batch_seq_id) AS
-- (
--     VALUES
--     ('event_value', 99, 1),
--     ('event_value', 100, 1),
--     ('event_value', 101, 2)
-- ),
-- child as (
--     insert into event_stats
--         (event_name_id, agg_window_id)
--     SELECT
--         event_name_id,
--         agg_window_id
--     from events
--     join event_names on event_names.event_name=events.event_name

--     returning event_id, batch_seq_id
-- )
-- insert into event_metrics (metric_id, child.event_id, value)
-- select * 
-- from metricc
-- join child on child.event_id=metrics.









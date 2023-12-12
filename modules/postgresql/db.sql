DROP TABLE IF EXISTS AGG_WINDOWS CASCADE;
CREATE TABLE AGG_WINDOWS (
    agg_window_id serial PRIMARY KEY,
    name VARCHAR,
    is_realtime integer
);

INSERT INTO agg_windows (agg_window_id, name)
VALUES 
(0, 'REALTIME'),
(1, 'MINUTE'),
(2, 'HOUR'),
(3, 'DAY'),
(4, 'MONTH');

DROP TABLE IF EXISTS event_names CASCADE;
CREATE TABLE event_names (
    event_name_id serial PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR
);

INSERT INTO event_names (event_name_id, name)
VALUES 
    (0, 'new_device'),
    (1, 'new_session'),
    (2, 'page_view'),
    (3, 'page_scroll'),
    (4, 'link_click')
    ;

DROP TABLE IF EXISTS loggers CASCADE;
CREATE TABLE loggers (
	logger_id serial PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    state_id INTEGER -- references()
);

INSERT INTO loggers (logger_id, name, description, state_id)
VALUES 
(0, 'default_logger', 'default', 1);

DROP TABLE IF EXISTS event_stats CASCADE;
CREATE TABLE event_stats (
	event_id serial PRIMARY KEY,
    lg_id INTEGER REFERENCES loggers (logger_id),
    en_id INTEGER REFERENCES EVENT_NAMES (event_name_id),
    ev_ts TIMESTAMP with time zone,
    aw_id INTEGER REFERENCES AGG_WINDOWS (agg_window_id),
    insertion_ts timestamp with time zone default NOW()
);

drop table if EXISTS event_dimensions;
create table event_dimensions (
    id serial primary key,
    dim_id integer, --REFERENCES dimensions(dim_id),
    event_id integer REFERENCES event_stats(event_id),
    value varchar
);

DROP TABLE IF EXISTS EVENT_METRICS CASCADE;
CREATE TABLE EVENT_METRICS (
    id serial PRIMARY KEY,
    metric_id integer, --REFERENCES metrics (metric_id),
    unit_id integer,
    event_id integer REFERENCES event_stats (event_id),
    value numeric not null
);





DROP TABLE IF EXISTS test CASCADE;
CREATE TABLE test (
	event_id serial PRIMARY KEY,
    val integer
);
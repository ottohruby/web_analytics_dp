DROP TABLE IF EXISTS analytics.loggers CASCADE;
CREATE TABLE analytics.loggers (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar,
    state_id integer
);

INSERT INTO analytics.loggers (id, name)
VALUES 
    (0, 'default')
    ;
DROP TABLE IF EXISTS analytics.states CASCADE;
CREATE TABLE analytics.states (
    id serial PRIMARY KEY,
    state_number integer not null,
    state_name varchar,
    changed_ts timestamp with time zone default current_timestamp
);

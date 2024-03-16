DROP TABLE IF EXISTS analytics.modules CASCADE;
CREATE TABLE analytics.modules (
    id serial PRIMARY KEY,
    name varchar unique not null,
    description varchar,
    state_id int REFERENCES analytics.states(id)
);


INSERT INTO analytics.modules (name, description) VALUES ('reports', '#graph-up');
INSERT INTO analytics.modules (name, description) VALUES ('users', '#people');
INSERT INTO analytics.modules (name, description) VALUES ('loggers', '#gear-wide-connected');
INSERT INTO analytics.modules (name, description) VALUES ('events', '#gear-wide-connected');
INSERT INTO analytics.modules (name, description) VALUES ('dimensions', '#gear-wide-connected');
INSERT INTO analytics.modules (name, description) VALUES ('metrics', '#gear-wide-connected');
INSERT INTO analytics.modules (name, description) VALUES ('units', '#gear-wide-connected');
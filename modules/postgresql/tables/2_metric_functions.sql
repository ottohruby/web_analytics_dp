DROP TABLE IF EXISTS analytics.metric_functions CASCADE;
CREATE TABLE analytics.metric_functions (
    id serial PRIMARY KEY,
    name varchar unique not null,
    description varchar,
    state_id int REFERENCES analytics.states(id)
);

INSERT INTO analytics.metric_functions (name, description) VALUES ('SUM', '');
INSERT INTO analytics.metric_functions (name, description) VALUES ('MIN', '');
INSERT INTO analytics.metric_functions (name, description) VALUES ('MAX', '');
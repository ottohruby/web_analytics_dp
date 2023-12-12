DROP TABLE IF EXISTS analytics.metrics CASCADE;
CREATE TABLE analytics.metrics (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar
);
INSERT INTO analytics.metrics (id, name)
VALUES 
    (0, 'count'),
    (1, 'value'),
    (2, 'quantity'),
    (3, 'position'),
    (4, 'percent')
    ;
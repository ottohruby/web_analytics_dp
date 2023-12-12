DROP TABLE IF EXISTS analytics.agg_windows CASCADE;
CREATE TABLE analytics.agg_windows (
    id serial PRIMARY KEY,
    name VARCHAR
);

INSERT INTO analytics.agg_windows (id, name)
VALUES 
(0, 'REALTIME'),
(1, 'MINUTE'),
(2, 'HOUR'),
(3, 'DAY'),
(4, 'MONTH');
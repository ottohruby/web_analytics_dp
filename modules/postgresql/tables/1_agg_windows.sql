DROP TABLE IF EXISTS analytics.agg_windows CASCADE;
CREATE TABLE analytics.agg_windows (
    id serial PRIMARY KEY,
    name VARCHAR
);

INSERT INTO analytics.agg_windows (name)
VALUES 
('REALTIME'),
('MINUTE'),
('HOUR'),
('DAY'),
('MONTH');
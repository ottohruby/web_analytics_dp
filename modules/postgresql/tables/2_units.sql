DROP TABLE IF EXISTS analytics.units CASCADE;
CREATE TABLE analytics.units (
    id serial PRIMARY KEY,
    base_unit_id integer REFERENCES analytics.units(id),
    name varchar not null,
    description varchar,
    is_base integer default(0),
    amount numeric not null default(1)
);
INSERT INTO analytics.units (id, base_unit_id, name, is_base, amount)
VALUES 
    (0, null, '-', 1, 1),
    (1, null, '%', 1, 1),
    (2, null, 'CZK', 1, 1)
    ;
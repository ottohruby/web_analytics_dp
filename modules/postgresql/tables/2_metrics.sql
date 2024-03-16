DROP TABLE IF EXISTS analytics.metrics CASCADE;
CREATE TABLE analytics.metrics (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar,
    base_unit_id int REFERENCES analytics.units(id),
    state_id int REFERENCES analytics.states(id)
);

DO $$
DECLARE
    state_id INTEGER;
BEGIN
	INSERT INTO analytics.states (state_number, state_name)
	VALUES (1, 'ACTIVE')
	RETURNING id INTO state_id;

	INSERT INTO analytics.metrics (name, description, base_unit_id, state_id)
	VALUES ('count', '', 1, state_id);

	INSERT INTO analytics.states (state_number, state_name)
	VALUES (1, 'ACTIVE')
	RETURNING id INTO state_id;

	INSERT INTO analytics.metrics (name, description, base_unit_id, state_id)
	VALUES ('value', '', 3, state_id);

	INSERT INTO analytics.states (state_number, state_name)
	VALUES (1, 'ACTIVE')
	RETURNING id INTO state_id;

	INSERT INTO analytics.metrics (name, description, base_unit_id, state_id)
	VALUES ('quantity', '', 1, state_id);

	INSERT INTO analytics.states (state_number, state_name)
	VALUES (1, 'ACTIVE')
	RETURNING id INTO state_id;

	INSERT INTO analytics.metrics (name, description, base_unit_id, state_id)
	VALUES ('position', '', 2, state_id);

	INSERT INTO analytics.states (state_number, state_name)
	VALUES (1, 'ACTIVE')
	RETURNING id INTO state_id;

	INSERT INTO analytics.metrics (name, description, base_unit_id, state_id)
	VALUES ('percent', '', 2, state_id);
END $$;
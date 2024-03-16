DROP TABLE IF EXISTS analytics.units CASCADE;
CREATE TABLE analytics.units (
    id serial PRIMARY KEY,
    base_unit_id integer REFERENCES analytics.units(id),
    name varchar not null,
    description varchar,
    is_base integer default(0),
    amount numeric not null default(1),
    state_id int REFERENCES analytics.states(id)
);


DO $$
DECLARE
    name text;
	state_id int;
BEGIN
    FOR name IN 
        SELECT UNNEST(ARRAY[
            '-', '%', 'CZK'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a dimension
	INSERT INTO analytics.units (name, description, amount, is_base, state_id)
	VALUES (name, '', 1, 1, state_id);
    END LOOP;
END $$;
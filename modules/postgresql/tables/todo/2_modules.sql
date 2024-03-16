DROP TABLE IF EXISTS analytics.modules CASCADE;
CREATE TABLE analytics.modules (
    id serial PRIMARY KEY,
    name varchar unique not null,
    description varchar,
    state_id int REFERENCES analytics.states(id)
);


DO $$
DECLARE
    name text;
    state_id int;
BEGIN
    FOR name IN 
        SELECT UNNEST(ARRAY[
            'reports', 'users', 'loggers', 'events', 'dimensions', 'metrics', 'units'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a module
	INSERT INTO analytics.modules (name, state_id)
	VALUES (name, state_id);
    END LOOP;
END $$;
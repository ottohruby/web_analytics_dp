DROP TABLE IF EXISTS analytics.loggers CASCADE;
CREATE TABLE analytics.loggers (
    id serial PRIMARY KEY,
    name varchar not null,
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
            'default'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a logger
	INSERT INTO analytics.loggers (name, description, state_id)
	VALUES (name, '', state_id);
    END LOOP;
END $$;
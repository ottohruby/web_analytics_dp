DROP TABLE IF EXISTS analytics.roles CASCADE;
CREATE TABLE analytics.roles (
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
            'Admin', 'Reports'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a dimension
	INSERT INTO analytics.roles (name, description, state_id)
	VALUES (name, '', state_id);
    END LOOP;
END $$;
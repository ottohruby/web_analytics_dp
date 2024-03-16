DROP TABLE IF EXISTS analytics.module_roles CASCADE;
CREATE TABLE analytics.module_roles (
    id serial PRIMARY KEY,
    role_id integer REFERENCES analytics.roles(id),
    module_id integer REFERENCES analytics.modules(id),
    state_id int REFERENCES analytics.states(id)
);

DO $$
DECLARE
    state_id int;
BEGIN
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a module
	INSERT INTO analytics.module_roles (role_id, module_id, state_id)
	VALUES (1, 1, state_id);
	
	-- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a module
	INSERT INTO analytics.module_roles (role_id, module_id, state_id)
	VALUES (2, 2, state_id);
END $$;
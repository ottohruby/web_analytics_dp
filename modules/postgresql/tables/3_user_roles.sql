DROP TABLE IF EXISTS analytics.user_roles CASCADE;
CREATE TABLE analytics.user_roles (
    id serial PRIMARY KEY,
    role_id integer REFERENCES analytics.roles(id),
    user_id integer REFERENCES analytics.users(user_id),
    state_id int REFERENCES analytics.states(id)
);

DO $$
DECLARE
    state_id int;
BEGIN
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'GRANTED')
        RETURNING id INTO state_id;
	
	-- Insert a user
	INSERT INTO analytics.user_roles (role_id, user_id, state_id)
	VALUES (1, 1, state_id);

        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'GRANTED')
        RETURNING id INTO state_id;
	
	-- Insert a user
	INSERT INTO analytics.user_roles (role_id, user_id, state_id)
	VALUES (2, 1, state_id);
END $$;
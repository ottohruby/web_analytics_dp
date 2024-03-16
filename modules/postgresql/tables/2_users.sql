DROP TABLE IF EXISTS analytics.users CASCADE;
CREATE TABLE analytics.users (
    user_id serial PRIMARY KEY,
    name varchar unique not null,
    email varchar unique,
    password_hash varchar not null,
    login_failed_attempts integer default 0,
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
	
	-- Insert a user
	INSERT INTO analytics.users (name, email, password_hash, login_failed_attempts, state_id)
	VALUES ('admin', '', 'pbkdf2:sha256:260000$LoJn4liECjx90xFh$5d91739d663d0da1c7615c1ccf6d589694b427da1a768408ee054b7f3f621a19', 0, state_id);

END $$;
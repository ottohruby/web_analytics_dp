DROP TABLE IF EXISTS analytics.dimensions CASCADE;
CREATE TABLE analytics.dimensions (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar,
    state_id int REFERENCES analytics.states(id)
);

DO $$
DECLARE
    dim_name text;
    state_id int;
BEGIN
    FOR dim_name IN 
        SELECT UNNEST(ARRAY[
            'visitor_id', 'device_type', 'page_domain', 'page_path', 'page_title',
            'page_referrer', 'session_id', 'session_source', 'session_medium',
            'session_campaign', 'link_url', 'item_id', 'item_name'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a dimension
	INSERT INTO analytics.dimensions (name, description, state_id)
	VALUES (dim_name, '', state_id);
    END LOOP;
END $$;
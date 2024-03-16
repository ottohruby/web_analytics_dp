DROP TABLE IF EXISTS analytics.event_names CASCADE;
CREATE TABLE analytics.event_names (
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
            'new_visitor', 'new_session', 'page_view', 'scroll', 'link_click',
            'purchase', 'view_item_detail', 'purchase_item', 'add_item_to_cart'
        ]) 
    LOOP
        -- Insert a state
        INSERT INTO analytics.states (state_number, state_name)
        VALUES (1, 'ACTIVE')
        RETURNING id INTO state_id;
	
	-- Insert a dimension
	INSERT INTO analytics.event_names (name, description, state_id)
	VALUES (name, '', state_id);
    END LOOP;
END $$;

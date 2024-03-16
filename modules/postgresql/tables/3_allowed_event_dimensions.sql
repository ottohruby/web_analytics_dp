DROP TABLE IF EXISTS analytics.allowed_event_dimensions CASCADE;
CREATE TABLE analytics.allowed_event_dimensions (
    id serial PRIMARY KEY,
    event_id int REFERENCES analytics.event_names(id),
    dimension_id int REFERENCES analytics.dimensions(id),
    state_id int REFERENCES analytics.states(id)
);

DO $$
DECLARE
    events TEXT[] := ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9];
    state_id INTEGER;
BEGIN
    FOR i IN 1..ARRAY_LENGTH(events, 1) LOOP
        DECLARE
            dimensions VARCHAR[];
        BEGIN
            SELECT ARRAY_AGG(value)
            FROM UNNEST(
                CASE i
                    WHEN 1 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'DISABLED', 'DISABLED', 'DISABLED']
                    WHEN 2 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'DISABLED', 'DISABLED', 'DISABLED']
                    WHEN 3 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'DISABLED', 'DISABLED', 'DISABLED']
                    WHEN 4 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'DISABLED', 'DISABLED', 'DISABLED']
                    WHEN 5 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'ALLOWED', 'DISABLED', 'DISABLED']
                    WHEN 6 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'DISABLED', 'DISABLED', 'DISABLED']
                    WHEN 7 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'ALLOWED', 'ALLOWED', 'ALLOWED']
                    WHEN 8 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'ALLOWED', 'ALLOWED', 'ALLOWED']
                    WHEN 9 THEN ARRAY['ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED','ALLOWED', 'ALLOWED', 'ALLOWED', 'ALLOWED']
                END
            ) AS t(value)
            INTO dimensions;
            
            FOR j IN 1..ARRAY_LENGTH(dimensions, 1) LOOP
		    	INSERT INTO analytics.states (state_number, state_name)
		    	VALUES (1, dimensions[j])
		    	RETURNING id INTO state_id;

				INSERT INTO analytics.allowed_event_dimensions (event_id, dimension_id, state_id)
                VALUES (i, j, state_id);
            END LOOP;
        END;
    END LOOP;
END $$;

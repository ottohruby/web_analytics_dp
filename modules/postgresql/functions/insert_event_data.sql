DROP TABLE IF EXISTS analytics.errors CASCADE;
CREATE TABLE analytics.errors (
    id SERIAL, 
    timestamp timestamp with time zone default current_timestamp, 
    message TEXT, 
    detail TEXT, 
    context TEXT);

CREATE OR REPLACE FUNCTION insert_event_data(
    lg_id integer,
    en_id integer,
    ev_ts timestamp with time zone,
    aw_id integer,
    dims jsonb[],
    metrics jsonb[]
)
RETURNS integer AS $$
DECLARE temp_event_id integer;
    _sql_state TEXT;
    _message TEXT;
    _detail TEXT;
    _hint TEXT;
    _context TEXT;
BEGIN
    -- Insert data into the event_stats table
    INSERT INTO analytics.event_stats (lg_id, en_id, ev_ts, aw_id)
    VALUES (lg_id, en_id, ev_ts, aw_id)
    RETURNING event_id INTO temp_event_id;

    -- Insert data into event_dimensions from the dims array
    FOR i IN 1..array_length(dims, 1)
    LOOP
        INSERT INTO analytics.event_dimensions (event_id, dim_id, value)
        VALUES (
			temp_event_id,
			(dims[i]->>'id')::integer, 
			(dims[i]->>'val')::varchar);
    END LOOP;

    -- Insert data into event_metrics from the metrics array
    FOR i IN 1..array_length(metrics, 1)
    LOOP
	if ((metrics[i]->>'function_id')::integer) is not null then
	        INSERT INTO analytics.event_metrics (event_id, metric_id, unit_id, value, function_id)
        	VALUES (
			temp_event_id,
			(metrics[i]->>'id')::integer, 
			(metrics[i]->>'unit')::integer, 
			(metrics[i]->>'val')::numeric,
			(metrics[i]->>'function_id')::integer);
	else
		INSERT INTO analytics.event_metrics (event_id, metric_id, unit_id, value, function_id)
		SELECT 
		    temp_event_id,
		    (metrics[i]->>'id')::integer, 
		    (metrics[i]->>'unit')::integer, 
		    (metrics[i]->>'val')::numeric,
		    a::integer AS function_id
		FROM 
		    unnest(ARRAY[1, 2, 3]) AS a;
	end if;
    END LOOP;

    return 1;

    EXCEPTION    
        WHEN OTHERS THEN

        GET STACKED DIAGNOSTICS
            _message := MESSAGE_TEXT,
            _detail := PG_EXCEPTION_DETAIL,
            _context := PG_EXCEPTION_CONTEXT;

        INSERT INTO analytics.errors (message, detail, context)
        VALUES (_message, _detail, _context);
        RETURN -1;
END;
$$ LANGUAGE plpgsql;

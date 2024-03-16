CREATE OR REPLACE FUNCTION process_event_data(input_aw_id integer DEFAULT 1) RETURNS VOID AS $$
DECLARE
    row_record RECORD;
    func_result INTEGER;
BEGIN
    FOR row_record IN 
 WITH new_events AS (
            SELECT 
                ev_ts,
                event_id,
                lg_id,
                en_id
            FROM 
                analytics.event_stats es
            WHERE   
                es.is_processed = 0
                AND es.aw_id = input_aw_id  
        ),
        allowed_dims AS (
            SELECT 
                new_events.event_id,
                array_agg(vals.dim_id ORDER BY dim_id) AS dim_ids,
                array_agg(vals.value ORDER BY dim_id) AS dim_vals,
                array_agg(jsonb_build_object('id', vals.dim_id, 'val', vals.value) ORDER BY vals.dim_id) AS dims
            FROM 
                new_events
            INNER JOIN analytics.allowed_event_dimensions allowed
                ON allowed.event_id = new_events.en_id
            INNER JOIN analytics.event_dimensions vals
                ON vals.dim_id = allowed.dimension_id
                AND new_events.event_id = vals.event_id
            GROUP BY 1
            ORDER BY 1
        ),
        allowed_metrics AS (
            SELECT 
                new_events.event_id,
                max(lg_id) AS lg_id,
                max(en_id) AS en_id,
                max(ev_ts) AS ev_ts,
                array_agg(vals.metric_id ORDER BY vals.metric_id) AS metric_ids,
                array_agg(vals.value ORDER BY vals.metric_id) AS metric_vals, -- todo conversion
                array_agg(jsonb_build_object('id', vals.metric_id, 'val', vals.value, 'unit', vals.unit_id, 'function_id', vals.function_id) ORDER BY vals.metric_id) AS metrics
            FROM 
                new_events
            INNER JOIN analytics.allowed_event_metrics allowed
                ON allowed.event_id = new_events.en_id
            INNER JOIN analytics.event_metrics vals
                ON vals.metric_id = allowed.metric_id
                AND new_events.event_id = vals.event_id
            GROUP BY 1
            ORDER BY 1
        ),
        base AS (
            SELECT 
                lg_id,
                en_id,
                CASE
                    WHEN input_aw_id = 1 THEN date_trunc('minute', ev_ts)
                    WHEN input_aw_id = 2 THEN date_trunc('hour', ev_ts)
                    WHEN input_aw_id = 3 THEN date_trunc('day', ev_ts)
                    WHEN input_aw_id = 4 THEN date_trunc('month', ev_ts)
                    ELSE date_trunc('minute', ev_ts)
                END AS ev_ts,
                allowed_dims.dims,
                jsonb_agg((metrics)) AS metrics,
                array_agg(allowed_metrics.event_id) AS event_ids
            FROM 
                allowed_metrics
            JOIN allowed_dims ON allowed_metrics.event_id = allowed_dims.event_id
            GROUP BY 1, 2, 3, 4
        ),
		final_events as(
		                SELECT 
                    lg_id,
                    ev_ts,
                    en_id,
                    dims,
                    event_ids,
                    (el->>'id') AS key,
                    (el->>'function_id') AS function_id,
                    max((el->>'unit')) AS unit,
					CASE
                        WHEN (el->>'function_id')::integer = 1 THEN SUM((el->>'val')::numeric)
                        WHEN (el->>'function_id')::integer = 2 THEN MIN((el->>'val')::numeric)
                        WHEN (el->>'function_id')::integer = 3 THEN MAX((el->>'val')::numeric)
                        ELSE 0
                    END as value
                FROM 
                    base, jsonb_array_elements(metrics) AS elem, jsonb_array_elements(elem) AS el
			    GROUP BY 
                    1, 2, 3, 4, 5, 6, 7
		)
        
        SELECT 
            lg_id,
            en_id,
            ev_ts,
            event_ids,
            dims,
            array_agg(jsonb_build_object(
                    'id', final_events.key,
                    'unit', final_events.unit,
                    'function_id', final_events.function_id,
                    'val', final_events.value
                    
                )) AS metrics
        FROM final_events
        GROUP BY 
            1, 2, 3, 4, 5


    LOOP
        BEGIN
            SELECT insert_event_data(
                row_record.lg_id, 
                row_record.en_id,
                row_record.ev_ts,
                input_aw_id + 1,
                row_record.dims,
                row_record.metrics)
            INTO func_result;

        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Exception message: %', SQLERRM;
        END;

        UPDATE analytics.event_stats
        SET is_processed = func_result
        WHERE event_id = ANY (row_record.event_ids);

    END LOOP;
END;
$$ LANGUAGE PLPGSQL;

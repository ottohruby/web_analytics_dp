CREATE OR REPLACE FUNCTION get_event_data(
    aw_id_param INT default 2,
    en_id_param INT default 3,
    lg_id_param INT default 1,
	dim_id_param INT[] default ARRAY[2, 3],
	metric_id_param INT[] default ARRAY[1],
	function_id_param INT[] default ARRAY[1],
    time_from_param TIMESTAMP WITH TIME ZONE default '2024-02-11 14:00:00'::TIMESTAMP WITH TIME ZONE,
    time_to_param TIMESTAMP WITH TIME ZONE default '2024-02-11 23:59:59'::TIMESTAMP WITH TIME ZONE
)
RETURNS TABLE (
    o_lg_id INTeger,
    o_ev_ts TIMESTAMP with time zone,
    o_event_name VARCHAR,
    o_dims JSONB[],
    o_metrics JSONB[]
) AS $$
BEGIN
    RETURN QUERY
 WITH new_events AS (
            SELECT 
                ev_ts,
                event_id,
                lg_id,
                en_id
            FROM 
                analytics.event_stats es
            WHERE 1=1   
                AND es.aw_id = aw_id_param
	 			and es.en_id = en_id_param
	 			and es.lg_id = lg_id_param
	            AND (time_from_param IS NULL OR es.ev_ts >= time_from_param)
                AND (time_to_param IS NULL OR es.ev_ts <= time_to_param)
        ),
        allowed_dims AS (
            SELECT 
                new_events.event_id,
                array_agg(vals.dim_id ORDER BY dim_id) AS dim_ids,
                array_agg(vals.value ORDER BY dim_id) AS dim_vals,
                array_agg(jsonb_build_object('id', dims.name, 'val', vals.value) ORDER BY vals.dim_id) AS dims
            FROM 
                new_events
            INNER JOIN analytics.allowed_event_dimensions allowed
                ON allowed.event_id = new_events.en_id
            INNER JOIN analytics.event_dimensions vals
                ON vals.dim_id = allowed.dimension_id
                AND new_events.event_id = vals.event_id
	    inner join analytics.dimensions dims
		on dims.id = vals.dim_id
WHERE COALESCE(array_length(dim_id_param, 1), 0) = 0 OR vals.dim_id = ANY(dim_id_param)
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
                array_agg(jsonb_build_object('id', metrics.name, 'val', vals.value, 'unit', units.name, 'function_id', vals.function_id) ORDER BY vals.metric_id) AS metrics
            FROM 
                new_events
            INNER JOIN analytics.allowed_event_metrics allowed
                ON allowed.event_id = new_events.en_id
            INNER JOIN analytics.event_metrics vals
                ON vals.metric_id = allowed.metric_id
                AND new_events.event_id = vals.event_id
			inner join analytics.metrics metrics
				on metrics.id = vals.metric_id
			inner join analytics.units units
				on units.id = vals.unit_id
and metrics.base_unit_id = units.id
		WHERE vals.metric_id = ANY(metric_id_param)
			and vals.function_id = ANY(function_id_param)
            GROUP BY 1
            ORDER BY 1
        ),
        base AS (
            SELECT 
                lg_id,
                en_id,
                CASE
                    WHEN aw_id_param = 2 THEN date_trunc('minute', ev_ts)
                    WHEN aw_id_param = 3 THEN date_trunc('hour', ev_ts)
                    WHEN aw_id_param = 4 THEN date_trunc('day', ev_ts)
                    WHEN aw_id_param = 5 THEN date_trunc('month', ev_ts)
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
		),
        final as(
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
			)
			
			select
	final.lg_id as _lg_id,
	final.ev_ts,
	en.name as event_name,
	final.dims,
	final.metrics
from final
left join analytics.event_names en
	on en.id=final.en_id
order by ev_ts asc;

END;
$$ LANGUAGE plpgsql;
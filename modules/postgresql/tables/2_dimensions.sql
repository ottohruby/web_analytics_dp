DROP TABLE IF EXISTS analytics.dimensions CASCADE;
CREATE TABLE analytics.dimensions (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar
);
INSERT INTO analytics.dimensions (id, name)
VALUES 
    (0, 'visitor_id'),
    (1, 'device_type'),
    (2, 'page_domain'),
    (3, 'page_path'),
    (4, 'page_title'),
    (5, 'page_referrer'),
    (6, 'session_id'),
    (7, 'session_source'),
    (8, 'session_medium'),
    (9, 'session_campaign'),
    (10, 'link_url'),
    (11, 'item_id'),
    (12, 'item_name')
    ;
DROP TABLE IF EXISTS analytics.event_names CASCADE;
CREATE TABLE analytics.event_names (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar
);
INSERT INTO analytics.event_names (id, name)
VALUES 
    (0, 'new_visitor'),
    (1, 'new_session'),
    (2, 'page_view'),
    (3, 'scroll'),
    (4, 'link_click'),
    (5, 'purchase'),
    (6, 'view_item_detail'),
    (7, 'purchase_item'),
    (8, 'add_item_to_cart')
    ;
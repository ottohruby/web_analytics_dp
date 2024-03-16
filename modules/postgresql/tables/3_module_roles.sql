DROP TABLE IF EXISTS analytics.module_roles CASCADE;
CREATE TABLE analytics.module_roles (
    id serial PRIMARY KEY,
    role_id integer REFERENCES analytics.roles(id),
    module_id integer REFERENCES analytics.modules(id)
);

INSERT INTO analytics.module_roles (role_id, module_id) VALUES (2, 1);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 2);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 3);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 4);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 5);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 6);
INSERT INTO analytics.module_roles (role_id, module_id) VALUES (1, 7);

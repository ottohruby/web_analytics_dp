DROP TABLE IF EXISTS analytics.reports CASCADE;
CREATE TABLE analytics.reports (
    id serial PRIMARY KEY,
    name varchar not null,
    description varchar,
    state_id int REFERENCES analytics.states(id),
    user_id int REFERENCES analytics.users(user_id),
    data JSON
);


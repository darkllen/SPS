INSERT INTO users (name, created_at)
SELECT
  'name' || s,
  NOW()
FROM generate_series(1, 100) as s;

psql -U postgres
CREATE USER reading_user WITH PASSWORD 'reading_pass';
GRANT CONNECT ON DATABASE my_database TO reading_user;
\connect my_database
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reading_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO reading_user;
GRANT USAGE ON SCHEMA public TO reading_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reading_user;


CREATE PUBLICATION my_events FOR TABLE events;
GRANT ALL ON events TO postgres;

CREATE PUBLICATION my_sensors FOR TABLE sensors;
GRANT ALL ON sensors TO postgres;

CREATE PUBLICATION my_users FOR TABLE users;
GRANT ALL ON users TO postgres;



CREATE SUBSCRIPTION my_sub_events CONNECTION 'dbname = postgres host = pg_m user = postgres password = pass' PUBLICATION my_events;
CREATE SUBSCRIPTION my_sub_sensors CONNECTION 'dbname = postgres host = pg_m user = postgres password = pass' PUBLICATION my_sensors;
CREATE SUBSCRIPTION my_sub_users CONNECTION 'dbname = postgres host = pg_m user = postgres password = pass' PUBLICATION my_users;


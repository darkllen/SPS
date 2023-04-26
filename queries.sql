INSERT INTO users (name, created_at)
SELECT
  'name' || generate_series(1, n),
  NOW()
FROM generate_series(1, n);

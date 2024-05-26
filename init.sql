DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'django') THEN
      CREATE ROLE django WITH LOGIN PASSWORD 'password';
   END IF;
END $$;

DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'courses') THEN
      CREATE DATABASE courses WITH OWNER django;
   END IF;
END $$;

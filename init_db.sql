DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'contacts') THEN
        CREATE TABLE contacts (
            user_id BIGINT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT
        );
    END IF;
END $$;

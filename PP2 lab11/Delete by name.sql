CREATE OR REPLACE PROCEDURE remove_contact_by_identifier(delete_identifier VARCHAR(100))
LANGUAGE plpgsql AS $$
BEGIN
    -- Delete by username
    IF EXISTS (SELECT 1 FROM contacts WHERE name = delete_identifier) THEN
        DELETE FROM contacts WHERE name = delete_identifier;
    -- Delete by phone
    ELSIF EXISTS (SELECT 1 FROM contacts WHERE phone = delete_identifier) THEN
        DELETE FROM contacts WHERE phone = delete_identifier;
    ELSE
        RAISE NOTICE 'No record found for deletion with identifier: %', delete_identifier;
    END IF;
END;
$$;

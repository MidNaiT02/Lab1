CREATE OR REPLACE PROCEDURE add_or_update_contact(new_name VARCHAR(100), new_phone VARCHAR(20))
LANGUAGE plpgsql AS $$
BEGIN
    -- Check if user exists by name
    IF EXISTS (SELECT 1 FROM contacts WHERE name = new_name) THEN
        -- Update the phone if user exists
        UPDATE contacts 
        SET phone = new_phone 
        WHERE name = new_name;
    ELSE
        -- Insert new user if they don't exist
        INSERT INTO contacts(name, phone)
        VALUES (new_name, new_phone);
    END IF;
END;
$$;

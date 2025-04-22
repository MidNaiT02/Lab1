CREATE OR REPLACE PROCEDURE insert_multiple_users(user_list TEXT[])
AS
$$
DECLARE
    user_record TEXT;
    user_name VARCHAR;
    user_phone VARCHAR;
BEGIN
    FOREACH user_record IN ARRAY user_list
    LOOP
        -- Extract name and phone from the string (assuming 'name:phone' format)
        user_name := split_part(user_record, ':', 1);
        user_phone := split_part(user_record, ':', 2);
        
        -- Check phone format (simple example: should be 10 digits)
        IF LENGTH(user_phone) = 10 AND user_phone ~ '^\d+$' THEN
            -- Insert user if phone format is correct
            INSERT INTO users (user_name, phone_number)
            VALUES (user_name, user_phone);
        ELSE
            -- Return incorrect data
            RAISE NOTICE 'Incorrect phone for user: %', user_name;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

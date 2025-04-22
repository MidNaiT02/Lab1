CREATE OR REPLACE PROCEDURE bulk_insert_contacts(users_list TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    user_record TEXT;
    user_name VARCHAR(100);
    user_phone VARCHAR(20);
BEGIN
    -- Loop through the users list
    FOREACH user_record IN ARRAY users_list LOOP
        -- Assuming each user in users_list is a comma-separated string: "name,phone"
        user_name := split_part(user_record, ',', 1);
        user_phone := split_part(user_record, ',', 2);

        -- Check if phone number is valid (simple validation)
        IF LENGTH(user_phone) < 10 THEN
            RAISE NOTICE 'Invalid phone number for user: %. Phone: %', user_name, user_phone;
        ELSE
            -- Insert or update user
            PERFORM add_or_update_contact(user_name, user_phone);
        END IF;
    END LOOP;
END;
$$;

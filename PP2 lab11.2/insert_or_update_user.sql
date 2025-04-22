CREATE OR REPLACE PROCEDURE insert_or_update_user(new_name VARCHAR, new_phone VARCHAR)
AS
$$
BEGIN
    -- If user already exists, update the phone number
    IF EXISTS (SELECT 1 FROM users WHERE user_name = new_name) THEN
        UPDATE users
        SET phone_number = new_phone
        WHERE user_name = new_name;
    ELSE
        -- If user does not exist, insert new user
        INSERT INTO users (user_name, phone_number)
        VALUES (new_name, new_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user_by_username_or_phone(input_value TEXT)
AS
$$
BEGIN
    -- Check if input_value is a valid phone number or username and delete the corresponding record
    IF input_value ~ '^\d+$' THEN
        DELETE FROM users
        WHERE phone_number = input_value;
    ELSE
        DELETE FROM users
        WHERE user_name = input_value;
    END IF;
END;
$$ LANGUAGE plpgsql;

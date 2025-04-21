CREATE OR REPLACE PROCEDURE delete_user(identifier TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM PhoneBook
    WHERE name = identifier OR phone = identifier;
END;
$$;

CREATE OR REPLACE PROCEDURE upsert_user(username TEXT, userphone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PhoneBook WHERE name = username) THEN
        UPDATE PhoneBook SET phone = userphone WHERE name = username;
    ELSE
        INSERT INTO PhoneBook(name, phone) VALUES (username, userphone);
    END IF;
END;
$$;

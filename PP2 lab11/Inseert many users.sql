CREATE OR REPLACE PROCEDURE insert_many_users(
    usernames TEXT[],
    userphones TEXT[],
    OUT invalid_entries TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT := 1;
BEGIN
    invalid_entries := ARRAY[]::TEXT[];

    WHILE i <= array_length(usernames, 1) LOOP
        IF userphones[i] ~ '^\+?\d{10,15}$' THEN
            -- Check existence and insert or update
            IF EXISTS (SELECT 1 FROM PhoneBook WHERE name = usernames[i]) THEN
                UPDATE PhoneBook SET phone = userphones[i] WHERE name = usernames[i];
            ELSE
                INSERT INTO PhoneBook(name, phone) VALUES (usernames[i], userphones[i]);
            END IF;
        ELSE
            invalid_entries := array_append(invalid_entries, usernames[i] || ' -> ' || userphones[i]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;

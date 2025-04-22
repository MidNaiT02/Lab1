CREATE OR REPLACE FUNCTION search_users(pattern TEXT)
RETURNS TABLE(id INT, user_name VARCHAR, phone_number VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT users.id, users.user_name, users.phone_number
    FROM users
    WHERE users.user_name ILIKE '%' || pattern || '%'
       OR users.phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

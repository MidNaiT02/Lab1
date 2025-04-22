CREATE OR REPLACE FUNCTION get_paginated_users(num_records INT, start_point INT)
RETURNS TABLE(id INT, user_name VARCHAR, phone_number VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT users.id, users.user_name, users.phone_number
    FROM users
    LIMIT num_records OFFSET start_point;
END;
$$ LANGUAGE plpgsql;
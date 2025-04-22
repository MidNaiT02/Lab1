CREATE FUNCTION paginate_contacts_query(limit_count INT, offset_count INT)
RETURNS TABLE(id INT, name VARCHAR(100), phone VARCHAR(20)) AS $$
BEGIN
    RETURN QUERY 
    SELECT id, name, phone
    FROM contacts
    ORDER BY id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;

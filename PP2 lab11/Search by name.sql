CREATE FUNCTION find_contacts_by_pattern(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR(100), phone VARCHAR(20)) AS $$
BEGIN
    RETURN QUERY 
    SELECT id, name, phone
    FROM contacts
    WHERE name LIKE '%' || pattern || '%' OR phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

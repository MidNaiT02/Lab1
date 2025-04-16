import psycopg2
 
conn = psycopg2.connect(host="localhost", dbname="labka10", user="postgres",
                        password="12345678", port=5432)   
 
cur = conn.cursor()
 
conn.set_session(autocommit=True)

cur.execute("""CREATE TABLE if not exists snake(
            name VARCHAR(255),
            level INTEGER,
            score INTEGER
);
           """)
#conn.commit()
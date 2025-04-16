
import psycopg2
from datetime import datetime

conn = psycopg2.connect(host="localhost", dbname = "labka10", user = "postgres",
                        password = "12345678", port = 5432)
cur = conn.cursor()

def get_or_create_user():
    username = input("Enter your username: ")
    cur.execute("SELECT id FROM game_user WHERE username = %s", (username,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO game_user (username) VALUES (%s)", (username,))
        conn.commit()
        print("🆕 New user added.")
        cur.execute("SELECT id FROM game_user WHERE username = %s", (username,))
        user = cur.fetchone()
    else:
        
        print("👋 Welcome back,", username)
    return user[0]

def save_score(user_id, level, score):
    cur.execute("""
        INSERT INTO user_score (user_id, level, score, saved_at)
        VALUES (%s, %s, %s, %s)
    """, (user_id, level, score, datetime.now()))
    conn.commit()
    print("💾 Score saved.")

def close_connection():
    cur.close()
    conn.close()
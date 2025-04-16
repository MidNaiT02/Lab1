CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY
);

CREATE TABLE user_scores (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) REFERENCES users(username),
    level INT,
    score INT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

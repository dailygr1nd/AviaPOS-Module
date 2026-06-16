CREATE TABLE IF NOT EXISTS auth_users (

    user_id TEXT PRIMARY KEY,

    merchant_id TEXT NOT NULL,

    username TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    role TEXT NOT NULL,

    active INTEGER DEFAULT 1,

    created_at TEXT NOT NULL
);
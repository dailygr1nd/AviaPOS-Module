CREATE TABLE IF NOT EXISTS users (

    user_id TEXT PRIMARY KEY,

    merchant_id TEXT NOT NULL,

    username TEXT NOT NULL,

    role TEXT NOT NULL,

    active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS merchants (

    merchant_id TEXT PRIMARY KEY,

    merchant_name TEXT NOT NULL,

    owner_name TEXT NOT NULL,

    phone TEXT NOT NULL,

    email TEXT,

    active INTEGER DEFAULT 1
);
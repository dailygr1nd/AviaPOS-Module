CREATE TABLE IF NOT EXISTS branches (

    branch_id TEXT PRIMARY KEY,

    merchant_id TEXT NOT NULL,

    branch_name TEXT NOT NULL,

    location TEXT,

    active INTEGER DEFAULT 1
);
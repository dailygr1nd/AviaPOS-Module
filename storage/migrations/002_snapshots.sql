CREATE TABLE IF NOT EXISTS snapshots (

    snapshot_id TEXT PRIMARY KEY,

    merchant_id TEXT NOT NULL,

    projection_name TEXT NOT NULL,

    snapshot_data TEXT NOT NULL,

    created_at TEXT NOT NULL
);
CREATE TABLE events (

    event_id TEXT PRIMARY KEY,

    merchant_id TEXT NOT NULL,

    event_type TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    previous_hash TEXT NOT NULL,

    payload_hash TEXT NOT NULL,

    payload TEXT NOT NULL,

    sync_status TEXT NOT NULL
);
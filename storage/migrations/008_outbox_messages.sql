CREATE TABLE IF NOT EXISTS outbox_messages (

    id BIGSERIAL PRIMARY KEY,

    message_id VARCHAR(100) UNIQUE NOT NULL,

    event_id VARCHAR(100) NOT NULL,

    event_type VARCHAR(100) NOT NULL,

    merchant_id VARCHAR(100) NOT NULL,

    aggregate_id VARCHAR(100) NOT NULL,

    payload JSONB NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',

    attempts INTEGER NOT NULL DEFAULT 0,

    last_error TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    published_at TIMESTAMP

);

CREATE INDEX IF NOT EXISTS idx_outbox_status
ON outbox_messages(status);

CREATE INDEX IF NOT EXISTS idx_outbox_merchant_id
ON outbox_messages(merchant_id);

CREATE INDEX IF NOT EXISTS idx_outbox_event_type
ON outbox_messages(event_type);

CREATE INDEX IF NOT EXISTS idx_outbox_created_at
ON outbox_messages(created_at);
CREATE TABLE IF NOT EXISTS idempotency_records (

    id BIGSERIAL PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    idempotency_key VARCHAR(150) NOT NULL,

    command_name VARCHAR(100) NOT NULL,

    request_hash VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',

    response_payload JSONB,

    error_message TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    completed_at TIMESTAMP,

    CONSTRAINT uq_idempotency_merchant_key
        UNIQUE (merchant_id, idempotency_key)

);

CREATE INDEX IF NOT EXISTS idx_idempotency_merchant_id
ON idempotency_records(merchant_id);

CREATE INDEX IF NOT EXISTS idx_idempotency_key
ON idempotency_records(idempotency_key);

CREATE INDEX IF NOT EXISTS idx_idempotency_status
ON idempotency_records(status);

CREATE INDEX IF NOT EXISTS idx_idempotency_command_name
ON idempotency_records(command_name);

CREATE INDEX IF NOT EXISTS idx_idempotency_created_at
ON idempotency_records(created_at);
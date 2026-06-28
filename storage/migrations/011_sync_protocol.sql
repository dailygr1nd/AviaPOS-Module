CREATE TABLE IF NOT EXISTS sync_devices (

    id BIGSERIAL PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100),

    user_id VARCHAR(100),

    device_id VARCHAR(150) NOT NULL,

    device_name VARCHAR(150),

    platform VARCHAR(50) NOT NULL DEFAULT 'ANDROID',

    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',

    last_seen_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_sync_device_merchant_device
        UNIQUE (merchant_id, device_id)

);

CREATE INDEX IF NOT EXISTS idx_sync_devices_merchant_id
ON sync_devices(merchant_id);

CREATE INDEX IF NOT EXISTS idx_sync_devices_branch_id
ON sync_devices(branch_id);

CREATE INDEX IF NOT EXISTS idx_sync_devices_user_id
ON sync_devices(user_id);

CREATE INDEX IF NOT EXISTS idx_sync_devices_status
ON sync_devices(status);

CREATE INDEX IF NOT EXISTS idx_sync_devices_created_at
ON sync_devices(created_at);


CREATE TABLE IF NOT EXISTS sync_inbox_events (

    id BIGSERIAL PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100),

    device_id VARCHAR(150) NOT NULL,

    client_event_id VARCHAR(150) NOT NULL,

    idempotency_key VARCHAR(200) NOT NULL,

    command_name VARCHAR(120) NOT NULL,

    payload JSONB NOT NULL,

    expected_version BIGINT,

    status VARCHAR(30) NOT NULL DEFAULT 'RECEIVED',

    error_message TEXT,

    occurred_at TIMESTAMP,

    received_at TIMESTAMP NOT NULL DEFAULT NOW(),

    processed_at TIMESTAMP,

    CONSTRAINT uq_sync_inbox_merchant_device_client_event
        UNIQUE (merchant_id, device_id, client_event_id)

);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_merchant_id
ON sync_inbox_events(merchant_id);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_branch_id
ON sync_inbox_events(branch_id);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_device_id
ON sync_inbox_events(device_id);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_client_event_id
ON sync_inbox_events(client_event_id);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_idempotency_key
ON sync_inbox_events(idempotency_key);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_command_name
ON sync_inbox_events(command_name);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_status
ON sync_inbox_events(status);

CREATE INDEX IF NOT EXISTS idx_sync_inbox_received_at
ON sync_inbox_events(received_at);
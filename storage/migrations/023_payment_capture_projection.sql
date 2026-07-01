CREATE TABLE IF NOT EXISTS payment_capture_projection (

    capture_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100),

    provider VARCHAR(100) NOT NULL,

    provider_channel VARCHAR(100) NOT NULL,

    provider_reference VARCHAR(255) NOT NULL,

    external_reference VARCHAR(255),

    payer_reference VARCHAR(255),

    payer_name VARCHAR(255),

    amount DOUBLE PRECISION NOT NULL,

    currency VARCHAR(3) NOT NULL,

    payment_method VARCHAR(100) NOT NULL,

    reference_type VARCHAR(100),

    reference_id VARCHAR(100),

    payment_id VARCHAR(100),

    railone_intent_id VARCHAR(255),

    status VARCHAR(50) NOT NULL,

    reconciliation_state VARCHAR(100) NOT NULL DEFAULT 'PENDING',

    reason VARCHAR(500),

    notes VARCHAR(500),

    raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,

    capture_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    version BIGINT NOT NULL DEFAULT 1,

    received_at TIMESTAMP NOT NULL DEFAULT NOW(),

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_payment_capture_merchant_provider_reference
        UNIQUE (merchant_id, provider, provider_reference)

);

CREATE INDEX IF NOT EXISTS idx_payment_capture_merchant_id
ON payment_capture_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_payment_capture_branch_id
ON payment_capture_projection(branch_id);

CREATE INDEX IF NOT EXISTS idx_payment_capture_provider
ON payment_capture_projection(provider);

CREATE INDEX IF NOT EXISTS idx_payment_capture_provider_channel
ON payment_capture_projection(provider_channel);

CREATE INDEX IF NOT EXISTS idx_payment_capture_provider_reference
ON payment_capture_projection(provider_reference);

CREATE INDEX IF NOT EXISTS idx_payment_capture_external_reference
ON payment_capture_projection(external_reference);

CREATE INDEX IF NOT EXISTS idx_payment_capture_payer_reference
ON payment_capture_projection(payer_reference);

CREATE INDEX IF NOT EXISTS idx_payment_capture_payment_method
ON payment_capture_projection(payment_method);

CREATE INDEX IF NOT EXISTS idx_payment_capture_reference_type
ON payment_capture_projection(reference_type);

CREATE INDEX IF NOT EXISTS idx_payment_capture_reference_id
ON payment_capture_projection(reference_id);

CREATE INDEX IF NOT EXISTS idx_payment_capture_payment_id
ON payment_capture_projection(payment_id);

CREATE INDEX IF NOT EXISTS idx_payment_capture_railone_intent_id
ON payment_capture_projection(railone_intent_id);

CREATE INDEX IF NOT EXISTS idx_payment_capture_status
ON payment_capture_projection(status);

CREATE INDEX IF NOT EXISTS idx_payment_capture_reconciliation_state
ON payment_capture_projection(reconciliation_state);

CREATE INDEX IF NOT EXISTS idx_payment_capture_received_at
ON payment_capture_projection(received_at);

CREATE INDEX IF NOT EXISTS idx_payment_capture_created_at
ON payment_capture_projection(created_at);

CREATE INDEX IF NOT EXISTS idx_payment_capture_updated_at
ON payment_capture_projection(updated_at);
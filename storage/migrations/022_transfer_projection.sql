CREATE TABLE IF NOT EXISTS transfer_projection (

    transfer_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    transfer_type VARCHAR(50) NOT NULL,

    status VARCHAR(50) NOT NULL,

    source_branch_id VARCHAR(100),

    destination_branch_id VARCHAR(100),

    destination_type VARCHAR(100),

    destination_reference VARCHAR(255),

    amount DOUBLE PRECISION,

    currency VARCHAR(3),

    purpose VARCHAR(255),

    rail_hint VARCHAR(100),

    external_reference VARCHAR(255),

    provider_reference VARCHAR(255),

    railone_intent_id VARCHAR(255),

    reconciliation_state VARCHAR(100),

    notes VARCHAR(500),

    reason VARCHAR(500),

    items JSONB NOT NULL DEFAULT '[]'::jsonb,

    dispatched_items JSONB NOT NULL DEFAULT '[]'::jsonb,

    received_items JSONB NOT NULL DEFAULT '[]'::jsonb,

    dispatched_by_user_id VARCHAR(100),

    received_by_user_id VARCHAR(100),

    transfer_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW()

);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_merchant_id
ON transfer_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_transfer_type
ON transfer_projection(transfer_type);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_status
ON transfer_projection(status);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_source_branch_id
ON transfer_projection(source_branch_id);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_destination_branch_id
ON transfer_projection(destination_branch_id);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_destination_type
ON transfer_projection(destination_type);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_destination_reference
ON transfer_projection(destination_reference);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_currency
ON transfer_projection(currency);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_rail_hint
ON transfer_projection(rail_hint);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_external_reference
ON transfer_projection(external_reference);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_provider_reference
ON transfer_projection(provider_reference);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_railone_intent_id
ON transfer_projection(railone_intent_id);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_reconciliation_state
ON transfer_projection(reconciliation_state);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_created_at
ON transfer_projection(created_at);

CREATE INDEX IF NOT EXISTS idx_transfer_projection_updated_at
ON transfer_projection(updated_at);
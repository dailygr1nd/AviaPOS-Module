ALTER TABLE payment_projection
ADD COLUMN IF NOT EXISTS version BIGINT NOT NULL DEFAULT 1;

CREATE INDEX IF NOT EXISTS idx_payment_projection_reference_id
ON payment_projection(reference_id);

CREATE INDEX IF NOT EXISTS idx_payment_projection_status
ON payment_projection(status);
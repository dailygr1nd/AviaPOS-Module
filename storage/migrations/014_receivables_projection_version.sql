ALTER TABLE receivable_projection
ADD COLUMN IF NOT EXISTS version BIGINT NOT NULL DEFAULT 1;

CREATE INDEX IF NOT EXISTS idx_receivable_projection_sale_id
ON receivable_projection(sale_id);

CREATE INDEX IF NOT EXISTS idx_receivable_projection_status
ON receivable_projection(status);
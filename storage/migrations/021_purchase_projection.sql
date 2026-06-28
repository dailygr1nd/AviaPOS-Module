CREATE TABLE IF NOT EXISTS purchase_projection (

    purchase_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100) NOT NULL,

    supplier_id VARCHAR(100) NOT NULL,

    supplier_invoice_ref VARCHAR(150),

    status VARCHAR(50) NOT NULL DEFAULT 'CREATED',

    total DOUBLE PRECISION NOT NULL DEFAULT 0,

    notes VARCHAR(500),

    lines JSONB NOT NULL DEFAULT '[]'::jsonb,

    received_items JSONB NOT NULL DEFAULT '[]'::jsonb,

    received_by_user_id VARCHAR(100),

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW()

);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_merchant_id
ON purchase_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_branch_id
ON purchase_projection(branch_id);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_supplier_id
ON purchase_projection(supplier_id);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_status
ON purchase_projection(status);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_supplier_invoice_ref
ON purchase_projection(supplier_invoice_ref);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_created_at
ON purchase_projection(created_at);

CREATE INDEX IF NOT EXISTS idx_purchase_projection_updated_at
ON purchase_projection(updated_at);
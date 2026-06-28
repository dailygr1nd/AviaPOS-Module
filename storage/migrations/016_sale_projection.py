CREATE TABLE IF NOT EXISTS sale_projection (

    sale_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100) NOT NULL,

    customer_id VARCHAR(100),

    payment_method VARCHAR(50) NOT NULL,

    total DOUBLE PRECISION NOT NULL DEFAULT 0,

    status VARCHAR(50) NOT NULL,

    lines JSONB NOT NULL DEFAULT '[]'::jsonb,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW()

);

CREATE INDEX IF NOT EXISTS idx_sale_projection_merchant_id
ON sale_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_sale_projection_branch_id
ON sale_projection(branch_id);

CREATE INDEX IF NOT EXISTS idx_sale_projection_customer_id
ON sale_projection(customer_id);

CREATE INDEX IF NOT EXISTS idx_sale_projection_payment_method
ON sale_projection(payment_method);

CREATE INDEX IF NOT EXISTS idx_sale_projection_status
ON sale_projection(status);

CREATE INDEX IF NOT EXISTS idx_sale_projection_created_at
ON sale_projection(created_at);
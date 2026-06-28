CREATE TABLE IF NOT EXISTS customer_projection (

    customer_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    name VARCHAR(255) NOT NULL,

    phone VARCHAR(50),

    email VARCHAR(255),

    address VARCHAR(500),

    customer_type VARCHAR(50) NOT NULL DEFAULT 'REGULAR',

    tax_id VARCHAR(100),

    credit_limit DOUBLE PRECISION NOT NULL DEFAULT 0,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_customer_projection_merchant_phone
        UNIQUE (merchant_id, phone),

    CONSTRAINT uq_customer_projection_merchant_email
        UNIQUE (merchant_id, email)

);

CREATE INDEX IF NOT EXISTS idx_customer_projection_merchant_id
ON customer_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_customer_projection_name
ON customer_projection(name);

CREATE INDEX IF NOT EXISTS idx_customer_projection_phone
ON customer_projection(phone);

CREATE INDEX IF NOT EXISTS idx_customer_projection_email
ON customer_projection(email);

CREATE INDEX IF NOT EXISTS idx_customer_projection_customer_type
ON customer_projection(customer_type);

CREATE INDEX IF NOT EXISTS idx_customer_projection_tax_id
ON customer_projection(tax_id);

CREATE INDEX IF NOT EXISTS idx_customer_projection_active
ON customer_projection(active);

CREATE INDEX IF NOT EXISTS idx_customer_projection_updated_at
ON customer_projection(updated_at);
CREATE TABLE IF NOT EXISTS supplier_projection (

    supplier_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    supplier_code VARCHAR(100),

    name VARCHAR(255) NOT NULL,

    contact_person VARCHAR(255),

    phone VARCHAR(50),

    email VARCHAR(255),

    address VARCHAR(500),

    tax_id VARCHAR(100),

    payment_terms VARCHAR(255),

    active BOOLEAN NOT NULL DEFAULT TRUE,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_supplier_projection_merchant_supplier_code
        UNIQUE (merchant_id, supplier_code),

    CONSTRAINT uq_supplier_projection_merchant_phone
        UNIQUE (merchant_id, phone),

    CONSTRAINT uq_supplier_projection_merchant_email
        UNIQUE (merchant_id, email)

);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_merchant_id
ON supplier_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_supplier_code
ON supplier_projection(supplier_code);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_name
ON supplier_projection(name);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_phone
ON supplier_projection(phone);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_email
ON supplier_projection(email);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_tax_id
ON supplier_projection(tax_id);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_active
ON supplier_projection(active);

CREATE INDEX IF NOT EXISTS idx_supplier_projection_updated_at
ON supplier_projection(updated_at);
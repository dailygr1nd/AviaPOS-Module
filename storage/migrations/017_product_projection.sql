CREATE TABLE IF NOT EXISTS product_projection (

    product_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    sku VARCHAR(100) NOT NULL,

    name VARCHAR(255) NOT NULL,

    selling_price DOUBLE PRECISION NOT NULL DEFAULT 0,

    cost_price DOUBLE PRECISION NOT NULL DEFAULT 0,

    category VARCHAR(100),

    barcode VARCHAR(100),

    active BOOLEAN NOT NULL DEFAULT TRUE,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_product_projection_merchant_sku
        UNIQUE (merchant_id, sku)

);

CREATE INDEX IF NOT EXISTS idx_product_projection_merchant_id
ON product_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_product_projection_sku
ON product_projection(sku);

CREATE INDEX IF NOT EXISTS idx_product_projection_name
ON product_projection(name);

CREATE INDEX IF NOT EXISTS idx_product_projection_category
ON product_projection(category);

CREATE INDEX IF NOT EXISTS idx_product_projection_barcode
ON product_projection(barcode);

CREATE INDEX IF NOT EXISTS idx_product_projection_active
ON product_projection(active);

CREATE INDEX IF NOT EXISTS idx_product_projection_updated_at
ON product_projection(updated_at);
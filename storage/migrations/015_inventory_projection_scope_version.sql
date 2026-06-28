CREATE TABLE IF NOT EXISTS inventory_projection (

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100) NOT NULL,

    product_id VARCHAR(100) NOT NULL,

    sku VARCHAR(100) NOT NULL,

    quantity INTEGER NOT NULL DEFAULT 0,

    last_cost_price DOUBLE PRECISION,

    version BIGINT NOT NULL DEFAULT 0,

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_inventory_projection
        PRIMARY KEY (merchant_id, branch_id, product_id)

);

ALTER TABLE inventory_projection
ADD COLUMN IF NOT EXISTS merchant_id VARCHAR(100) DEFAULT 'LEGACY_MERCHANT';

ALTER TABLE inventory_projection
ADD COLUMN IF NOT EXISTS sku VARCHAR(100) DEFAULT 'UNKNOWN';

ALTER TABLE inventory_projection
ADD COLUMN IF NOT EXISTS last_cost_price DOUBLE PRECISION;

ALTER TABLE inventory_projection
ADD COLUMN IF NOT EXISTS version BIGINT NOT NULL DEFAULT 0;

ALTER TABLE inventory_projection
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW();

ALTER TABLE inventory_projection
DROP CONSTRAINT IF EXISTS inventory_projection_pkey;

ALTER TABLE inventory_projection
DROP CONSTRAINT IF EXISTS pk_inventory_projection;

ALTER TABLE inventory_projection
ALTER COLUMN merchant_id SET NOT NULL;

ALTER TABLE inventory_projection
ALTER COLUMN branch_id SET NOT NULL;

ALTER TABLE inventory_projection
ALTER COLUMN product_id SET NOT NULL;

ALTER TABLE inventory_projection
ADD CONSTRAINT pk_inventory_projection
PRIMARY KEY (merchant_id, branch_id, product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_projection_merchant_id
ON inventory_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_inventory_projection_branch_id
ON inventory_projection(branch_id);

CREATE INDEX IF NOT EXISTS idx_inventory_projection_product_id
ON inventory_projection(product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_projection_sku
ON inventory_projection(sku);

CREATE INDEX IF NOT EXISTS idx_inventory_projection_updated_at
ON inventory_projection(updated_at);
CREATE TABLE IF NOT EXISTS branch_projection (

    branch_id VARCHAR(100) PRIMARY KEY,

    merchant_id VARCHAR(100) NOT NULL,

    branch_code VARCHAR(100),

    name VARCHAR(255) NOT NULL,

    location VARCHAR(255) NOT NULL,

    phone VARCHAR(50),

    address VARCHAR(500),

    manager_user_id VARCHAR(100),

    active BOOLEAN NOT NULL DEFAULT TRUE,

    version BIGINT NOT NULL DEFAULT 1,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_branch_projection_merchant_branch_code
        UNIQUE (merchant_id, branch_code)

);

CREATE INDEX IF NOT EXISTS idx_branch_projection_merchant_id
ON branch_projection(merchant_id);

CREATE INDEX IF NOT EXISTS idx_branch_projection_branch_code
ON branch_projection(branch_code);

CREATE INDEX IF NOT EXISTS idx_branch_projection_name
ON branch_projection(name);

CREATE INDEX IF NOT EXISTS idx_branch_projection_location
ON branch_projection(location);

CREATE INDEX IF NOT EXISTS idx_branch_projection_manager_user_id
ON branch_projection(manager_user_id);

CREATE INDEX IF NOT EXISTS idx_branch_projection_active
ON branch_projection(active);

CREATE INDEX IF NOT EXISTS idx_branch_projection_updated_at
ON branch_projection(updated_at);
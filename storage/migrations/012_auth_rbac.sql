CREATE TABLE IF NOT EXISTS auth_users (

    id BIGSERIAL PRIMARY KEY,

    user_id VARCHAR(100) UNIQUE NOT NULL,

    merchant_id VARCHAR(100) NOT NULL,

    branch_id VARCHAR(100),

    username VARCHAR(100) NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    role VARCHAR(50) NOT NULL,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_auth_users_merchant_username
        UNIQUE (merchant_id, username)

);

CREATE INDEX IF NOT EXISTS idx_auth_users_user_id
ON auth_users(user_id);

CREATE INDEX IF NOT EXISTS idx_auth_users_merchant_id
ON auth_users(merchant_id);

CREATE INDEX IF NOT EXISTS idx_auth_users_branch_id
ON auth_users(branch_id);

CREATE INDEX IF NOT EXISTS idx_auth_users_username
ON auth_users(username);

CREATE INDEX IF NOT EXISTS idx_auth_users_role
ON auth_users(role);

CREATE INDEX IF NOT EXISTS idx_auth_users_active
ON auth_users(active);
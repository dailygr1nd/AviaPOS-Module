CREATE TABLE IF NOT EXISTS projections (

    projection_name TEXT NOT NULL,

    merchant_id TEXT NOT NULL,

    projection_data TEXT NOT NULL,

    updated_at TEXT NOT NULL,

    PRIMARY KEY (
        projection_name,
        merchant_id
    )
);
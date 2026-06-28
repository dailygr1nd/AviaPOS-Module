CREATE UNIQUE INDEX IF NOT EXISTS uq_events_merchant_aggregate_version
ON events (
    merchant_id,
    aggregate_id,
    version
);

# AviaPOS Architecture

## What AviaPOS Is

AviaPOS is a Merchant Operating System designed for African SMEs.

It is intentionally not an ERP.

The platform focuses on four core merchant activities:

1. Sales
2. Inventory
3. Expenses
4. Receivables

These four domains provide the majority of operational visibility required by small and medium businesses.

---

## Architectural Principles

### Event-First

Business actions generate immutable events.

Examples:

- Sale Created
- Inventory Received
- Expense Recorded
- Debt Created

Events become the source of truth.

---

### PostgreSQL as System of Record

PostgreSQL stores:

- Event Store
- Snapshots
- Projections
- Merchant Metadata

The database is the authoritative ledger.

---

### Redis as Event Transport

Redis Streams distribute events to workers.

This enables:

- Asynchronous projections
- Background processing
- Future RailOne integration
- Horizontal scaling

---

### Offline First

AviaPOS is designed to operate in environments with unreliable connectivity.

Future mobile clients maintain a local event store and synchronize business events when connectivity becomes available.

Synchronization is event-based rather than state-based.

---

### Snapshot-Based Recovery

Aggregates are periodically snapshotted.

Recovery flow:

Snapshot
→ Load State
→ Replay Remaining Events

instead of replaying the entire event history.

---

### RailOne Compatibility

AviaPOS is designed to integrate with RailOne without custody of customer funds.

AviaPOS produces business events.

RailOne handles routing, settlement, liquidity visibility, and payment orchestration.


## Core Business Domains

AviaPOS intentionally focuses on four merchant domains:

### Sales

Tracks money entering the business.

### Inventory

Tracks stock movement and inventory valuation.

### Expenses

Tracks money leaving the business.

### Receivables

Tracks money owed to the business.

Together these provide a complete operational picture for most SMEs without introducing ERP-level complexity.

## Future RailOne Integration

RailOne will provide:

- Payment Routing
- Settlement Verification
- Reconciliation
- Liquidity Visibility
- Multi-Rail Connectivity

without taking custody of merchant funds.

---

## Technology Stack

Backend

- Python 3.12+
- FastAPI
- PostgreSQL
- Redis
- Event Sourcing

Future

- RailOne Connectors

## Reliability Pattern: Unit of Work + Outbox

AviaPOS uses the Outbox Pattern for reliable event publication.

When a command is handled, the system writes both the domain event and the outbox message in the same PostgreSQL transaction.

```text
Command Handler
    ↓
Unit of Work
    ↓
events table
    +
outbox_messages table
    ↓
commit


## Reliability Pattern: Idempotency Keys

All write endpoints must support idempotency.

Flutter and offline-first clients may retry requests when connectivity is unstable.

To prevent duplicate writes, every command request should include:

```text
Idempotency-Key: <client-generated-unique-key>


## Reliability Pattern: Optimistic Concurrency

AviaPOS uses optimistic concurrency to protect aggregate updates.

Every event has an aggregate version.

For updates to an existing aggregate, the client must send:

```text
X-Expected-Version: <current-version-known-by-client>


## Reliability Pattern: Hash Chain Verification

AviaPOS events are hash-chained.

Each event stores:

- previous_hash
- current_hash
- payload
- event_type
- merchant_id

The verifier recomputes the event hash from the stored event payload and confirms that:

1. The event payload has not been altered.
2. The stored current_hash is correct.
3. The event previous_hash links to the prior merchant event.
4. The merchant event stream is intact from GENESIS onward.

Control Center endpoints:

```text
GET /control/integrity/merchant/{merchant_id}
GET /control/integrity/aggregate/{merchant_id}/{aggregate_id}


## Offline Sync Protocol

AviaPOS is designed for offline-first operation.

Android clients should maintain a local SQLite event/command queue.

When the device is offline, business actions are stored locally.

When connectivity returns, the device pushes pending client events to AviaPOS.

```text
Android SQLite
    ↓
POST /sync/push
    ↓
sync_inbox_events



## Auth and RBAC

AviaPOS uses merchant-scoped authentication.

Each user belongs to a merchant and has a role.

Supported roles:

- OWNER
- MANAGER
- CASHIER
- INVENTORY_CLERK
- ACCOUNTANT

Flutter authenticates using:

```text
POST /auth/login
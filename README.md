
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

# AviaPOS

AviaPOS is a lightweight Merchant Operating System (Merchant OS) built by Avia Technologies.

The platform is designed for African SMEs that require reliable sales tracking, inventory management, debt management, branch operations, and financial visibility without the complexity of traditional ERP systems.

---

## Core Principles

### Event-First Design

Every business operation is recorded as a business event.

Examples:

- Sale Created
- Inventory Added
- Inventory Deducted
- Debt Created
- Debt Settled
- Branch Transfer Created

The event stream acts as the source of truth.

---

### Hash-Chained Business Events

Business events are cryptographically linked.

Benefits:

- Auditability
- Tamper Detection
- Reliable Business History
- Event Integrity

Only business-critical events are hash chained.

---

### Lightweight Merchant OS

AviaPOS intentionally avoids ERP bloat.

Included:

- Sales
- Inventory
- Debts
- Expenses
- Suppliers
- Branch Operations
- Dashboards

Excluded:

- Payroll
- HR
- Recruitment
- Marketing Automation
- CRM Complexity

---

### Offline-First

Merchants can continue operating without internet access.

The Sync Engine allows:

- Desktop Sync
- Mobile Sync
- Branch Sync
- Future RailOne Sync

---

### Privacy-First Identity

AviaPOS does not perform identity verification directly.

Identity verification is delegated to trusted third-party issuers.

AviaPOS only stores verification references and permissions.

---

### Non-Custodial By Design

AviaPOS does not hold customer funds.

Financial assets remain within regulated institutions.

Future payment orchestration is handled through RailOne.

---
## Financial Architecture

AviaPOS separates business activity from payment activity.

Business domains:

- Sales
- Inventory
- Expenses
- Receivables
- Payables

do not directly move money.

All financial settlement flows through the Payment Domain.

Examples:

SALE
→ PAYMENT

RECEIVABLE
→ PAYMENT

PAYABLE
→ PAYMENT

EXPENSE
→ PAYMENT

This creates a single financial language across the platform and simplifies future RailOne integration.

---

## Design Goal

AviaPOS is not intended to become an ERP.

It is intended to become a Merchant Operating System.

The platform focuses on the smallest set of operational primitives required to run an SME:

- Sales
- Inventory
- Expenses
- Receivables
- Payables
- Payments

Everything else should be implemented only if it directly supports one of these domains.





---

## Modules

## Sales

Records sales transactions and receipts.

## Inventory

Tracks stock movement and availability.

### Debts

Tracks customer credit and settlements.

### Transfers

Tracks branch-to-branch operational transfers.

### Suppliers

Tracks supplier obligations.

## Expenses

Tracks operational spending.

---

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
- SQLite
- Event Sourcing

Future

- PostgreSQL
- Redis
- RailOne Connectors

---

## Status

Current Phase:

MVP Foundation

Implemented:

- Event Ledger
- Hash Chaining
- Projections
- Sync Engine
- Core Business Modules

In Progress:

- API Layer
- Authentication
- Dashboard APIs

Future:

- Multi-Branch Operations
- Supplier Management
- Expense Management
- RailOne Integration
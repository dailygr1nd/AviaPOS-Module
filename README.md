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

## Architecture





---

## Modules

### Sales

Records sales transactions and receipts.

### Inventory

Tracks stock movement and availability.

### Debts

Tracks customer credit and settlements.

### Transfers

Tracks branch-to-branch operational transfers.

### Suppliers

Tracks supplier obligations.

### Expenses

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
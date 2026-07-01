# AviaPOS Flutter API Contract

## Status

Flutter integration baseline for the current AviaPOS backend.

This contract reflects the current active runtime:

```text
Auth
Dashboard
Branches
Products
Customers
Suppliers
Purchases
Transfers
Sales
Inventory
Expenses
Payments
Receivables
Sync
Integrity
```

---

# 1. System Positioning

AviaPOS is the merchant operating layer.

RailOne is the future non-custodial routing, execution, continuity, settlement-reference, and reconciliation layer.

Avia Technologies is non-custodial by design.

AviaPOS must never be treated as:

```text
a wallet
a custodian
a stored-value account
a holder of merchant funds
a holder of customer funds
```

AviaPOS records:

```text
commercial events
operational events
merchant payment capture events
expected settlement amounts
external rail references
provider confirmations
RailOne intent references
reconciliation state
stock movement state
branch movement state
```

AviaPOS does not record:

```text
Avia wallet balance
customer wallet balance
merchant wallet balance
funds held by Avia
```

---

# 2. Runtime Architecture

All production writes follow this path:

```text
Flutter Client
    ↓
FastAPI Module API
    ↓
Command Bus
    ↓
Command Handler
    ↓
UnitOfWork
    ↓
PostgreSQL Event Store
    ↓
Outbox
    ↓
Redis Streams
    ↓
Projection Workers / Reaction Workers
    ↓
Read Projections
```

PostgreSQL is the source of truth.

Redis is transport only.

Flutter does not connect directly to PostgreSQL or Redis.

---

# 3. Deprecated Paths

Flutter must not call or depend on:

```text
api/routes/*
app_context.py
application/*
storage/sqlite/*
core.ledger.store
modules.debts/*
legacy service files
legacy in-memory projections
```

Debt is deprecated in favor of:

```text
Receivables
Payables later
```

---

# 4. General API Rules

## 4.1 Base Headers

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

Command/write endpoints require:

```text
Idempotency-Key: <client-generated-key>
```

Update/state-transition endpoints require:

```text
X-Expected-Version: <current_known_version>
```

---

## 4.2 Merchant Scope

Most requests include:

```json
{
  "merchant_id": "M001"
}
```

Flutter must not allow users to manually change `merchant_id`.

Flutter should load the active merchant from:

```text
GET /auth/me
```

---

## 4.3 Branch Scope

Branch-scoped modules include:

```text
Dashboard
Sales
Inventory
Purchases
Transfers
Expenses
Receivables
Users
```

Flutter should keep the active branch in local application state after login.

---

## 4.4 Idempotency

Every command/write request must include an `Idempotency-Key`.

Recommended format:

```text
<merchant_id>-<device_id>-<domain>-<local_sequence>
```

Examples:

```text
M001-POS01-SALE-000001
M001-POS01-PROD-000001
M001-POS01-CUST-000001
M001-POS01-SUP-000001
M001-POS01-PUR-000001
M001-POS01-TRF-000001
M001-POS01-FUNDS-000001
```

Idempotency protects against:

```text
offline retry
network timeout
double tap
app restart
sync replay
duplicate command submission
```

---

## 4.5 Optimistic Concurrency

State-changing endpoints require:

```text
X-Expected-Version: <version>
```

Flutter gets `version` from read endpoints.

When the backend returns:

```text
409 Conflict
```

Flutter should refresh the resource and let the user retry.

When the backend returns:

```text
428 Precondition Required
```

Flutter forgot to send `X-Expected-Version`.

---

## 4.6 Common Errors

```text
400 Bad Request
```

Invalid payload or business rule violation.

```text
401 Unauthorized
```

Missing, invalid, or expired token.

```text
403 Forbidden
```

Authenticated user does not have merchant/resource access.

```text
404 Not Found
```

Resource does not exist.

```text
409 Conflict
```

Idempotency conflict, command already in progress, or optimistic concurrency failure.

```text
428 Precondition Required
```

Missing `X-Expected-Version`.

---

# 5. Recommended Flutter Startup Flow

```text
1. Open app
2. Load saved token from secure storage
3. GET /auth/me
4. Load merchant_id, role, branch_id
5. Register or refresh device using /sync/devices/register
6. Pull server events using /sync/pull/{merchant_id}
7. Load dashboard using /dashboard/{merchant_id}
8. Load branches
9. Load products
10. Load customers
11. Load suppliers
12. Load inventory for active branch
13. Load pending local events
14. Resume offline sync queue
```

---

# 6. Recommended Merchant Onboarding Flow

```text
1. Bootstrap owner
2. Login owner
3. Create branches
4. Create users / cashiers
5. Create products
6. Receive opening stock
7. Create customers
8. Create suppliers
9. Start sales
10. Start purchases
11. Start stock transfers
12. Capture payment references
13. Use funds movement intents for supplier/branch payment instructions
14. Reconcile through provider references / RailOne references later
```

---

# 7. Auth

## 7.1 Bootstrap Owner

Used once when a merchant has no users.

```text
POST /auth/bootstrap-owner
```

### Body

```json
{
  "merchant_id": "M001",
  "username": "owner",
  "password": "password123"
}
```

### Response

```json
{
  "user_id": "...",
  "merchant_id": "M001",
  "username": "owner",
  "role": "OWNER",
  "branch_id": null,
  "active": true
}
```

---

## 7.2 Login

```text
POST /auth/login
```

### Body

```json
{
  "merchant_id": "M001",
  "username": "owner",
  "password": "password123"
}
```

### Response

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Flutter should store the token securely.

---

## 7.3 Current User

```text
GET /auth/me
```

### Headers

```text
Authorization: Bearer <token>
```

### Response

```json
{
  "user_id": "...",
  "merchant_id": "M001",
  "username": "owner",
  "role": "OWNER",
  "branch_id": null,
  "active": true
}
```

---

## 7.4 Create User

```text
POST /auth/users
```

### Headers

```text
Authorization: Bearer <token>
```

### Body

```json
{
  "merchant_id": "M001",
  "username": "cashier1",
  "password": "password123",
  "role": "CASHIER",
  "branch_id": "B001"
}
```

### Supported Roles

```text
OWNER
MANAGER
CASHIER
INVENTORY_CLERK
ACCOUNTANT
```

---

# 8. Dashboard

Dashboard is read-only.

It reads projection tables.

It does not dispatch commands.

---

## 8.1 Merchant Dashboard

```text
GET /dashboard/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

### Response Shape

```json
{
  "merchant_id": "M001",
  "branch_id": null,
  "sales": {},
  "inventory": {},
  "cashflow": {},
  "receivables": {},
  "expenses": {},
  "payments": {},
  "warnings": []
}
```

---

## 8.2 Branch Dashboard

```text
GET /dashboard/{merchant_id}/branch/{branch_id}
```

### Headers

```text
Authorization: Bearer <token>
```

Branch dashboard is scoped where projections support branch-level reads.

---

# 9. Branches

Branches are merchant-scoped operating locations.

Branches are used by:

```text
Sales
Inventory
Purchases
Transfers
Expenses
Receivables
Dashboard
Users
```

Branch responses include `version`.

Flutter must use `version` as `X-Expected-Version` when updating or deactivating branches.

---

## 9.1 Create Branch

```text
POST /branches
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-BRANCH-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_code": "MAIN",
  "name": "Main Branch",
  "location": "Dar es Salaam",
  "phone": "+255700000000",
  "address": "City Centre",
  "manager_user_id": null
}
```

### Response

```json
{
  "success": true,
  "branch_id": "...",
  "event_id": "...",
  "event_type": "BRANCH_CREATED",
  "version": 1
}
```

---

## 9.2 Update Branch

```text
PATCH /branches
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-BRANCH-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "...",
  "location": "Arusha"
}
```

---

## 9.3 Deactivate Branch

```text
POST /branches/deactivate
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-BRANCH-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "...",
  "reason": "Branch closed"
}
```

---

## 9.4 List Branches

```text
GET /branches/{merchant_id}
```

Optional:

```text
?include_inactive=true
```

---

## 9.5 Search Branches

```text
GET /branches/{merchant_id}/search?q=main
```

---

## 9.6 Branch Detail

```text
GET /branches/{merchant_id}/{branch_id}
```

### Response Shape

```json
{
  "branch_id": "...",
  "merchant_id": "M001",
  "branch_code": "MAIN",
  "name": "Main Branch",
  "location": "Dar es Salaam",
  "phone": "+255700000000",
  "address": "City Centre",
  "manager_user_id": null,
  "active": true,
  "version": 1,
  "created_at": "...",
  "updated_at": "..."
}
```

---

# 10. Products

Products are merchant-scoped reference data.

Products are used by:

```text
Sales
Inventory
Purchases
Transfers
```

Product responses include `version`.

---

## 10.1 Create Product

```text
POST /products
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PROD-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "sku": "SODA-500ML",
  "name": "Soda 500ml",
  "selling_price": 100,
  "cost_price": 70,
  "category": "Drinks",
  "barcode": "123456789"
}
```

### Response

```json
{
  "success": true,
  "product_id": "...",
  "event_id": "...",
  "event_type": "PRODUCT_CREATED",
  "version": 1
}
```

---

## 10.2 Update Product

```text
PATCH /products
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PROD-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "product_id": "...",
  "selling_price": 120
}
```

---

## 10.3 Deactivate Product

```text
POST /products/deactivate
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PROD-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "product_id": "...",
  "reason": "No longer sold"
}
```

---

## 10.4 List Products

```text
GET /products/{merchant_id}
```

Optional:

```text
?include_inactive=true
```

---

## 10.5 Search Products

```text
GET /products/{merchant_id}/search?q=soda
```

---

## 10.6 Product by SKU

```text
GET /products/{merchant_id}/sku/{sku}
```

---

## 10.7 Product Detail

```text
GET /products/{merchant_id}/{product_id}
```

### Response Shape

```json
{
  "product_id": "...",
  "merchant_id": "M001",
  "sku": "SODA-500ML",
  "name": "Soda 500ml",
  "selling_price": 100,
  "cost_price": 70,
  "category": "Drinks",
  "barcode": "123456789",
  "active": true,
  "version": 1,
  "created_at": "...",
  "updated_at": "..."
}
```

---

# 11. Customers

Customers are merchant-scoped reference data.

Customers are used by:

```text
Sales
Receivables
Credit sales
```

Customer responses include `version`.

---

## 11.1 Create Customer

```text
POST /customers
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "name": "John Doe",
  "phone": "+255700000000",
  "email": "john@example.com",
  "address": "Dar es Salaam",
  "customer_type": "REGULAR",
  "tax_id": null,
  "credit_limit": 0
}
```

### Response

```json
{
  "success": true,
  "customer_id": "...",
  "event_id": "...",
  "event_type": "CUSTOMER_CREATED",
  "version": 1
}
```

---

## 11.2 Update Customer

```text
PATCH /customers
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "customer_id": "...",
  "phone": "+255711111111",
  "credit_limit": 100000
}
```

---

## 11.3 Deactivate Customer

```text
POST /customers/deactivate
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "customer_id": "...",
  "reason": "Duplicate account"
}
```

---

## 11.4 List Customers

```text
GET /customers/{merchant_id}
```

Optional:

```text
?include_inactive=true
```

---

## 11.5 Search Customers

```text
GET /customers/{merchant_id}/search?q=john
```

---

## 11.6 Customer Detail

```text
GET /customers/{merchant_id}/{customer_id}
```

### Response Shape

```json
{
  "customer_id": "...",
  "merchant_id": "M001",
  "name": "John Doe",
  "phone": "+255700000000",
  "email": "john@example.com",
  "address": "Dar es Salaam",
  "customer_type": "REGULAR",
  "tax_id": null,
  "credit_limit": 0,
  "active": true,
  "version": 1,
  "created_at": "...",
  "updated_at": "..."
}
```

---

# 12. Suppliers

Suppliers are merchant-scoped reference data.

Suppliers are used by:

```text
Purchases
Supplier payment intents
Future payables
```

Supplier responses include `version`.

---

## 12.1 Create Supplier

```text
POST /suppliers
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "supplier_code": "ACME",
  "name": "ACME Supplies",
  "contact_person": "Jane Doe",
  "phone": "+255700000000",
  "email": "jane@acme.example",
  "address": "Dar es Salaam",
  "tax_id": "TIN123",
  "payment_terms": "NET_30"
}
```

### Response

```json
{
  "success": true,
  "supplier_id": "...",
  "event_id": "...",
  "event_type": "SUPPLIER_CREATED",
  "version": 1
}
```

---

## 12.2 Update Supplier

```text
PATCH /suppliers
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "supplier_id": "...",
  "payment_terms": "NET_14"
}
```

---

## 12.3 Deactivate Supplier

```text
POST /suppliers/deactivate
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "supplier_id": "...",
  "reason": "No longer active"
}
```

---

## 12.4 List Suppliers

```text
GET /suppliers/{merchant_id}
```

Optional:

```text
?include_inactive=true
```

---

## 12.5 Search Suppliers

```text
GET /suppliers/{merchant_id}/search?q=acme
```

---

## 12.6 Supplier Detail

```text
GET /suppliers/{merchant_id}/{supplier_id}
```

### Response Shape

```json
{
  "supplier_id": "...",
  "merchant_id": "M001",
  "supplier_code": "ACME",
  "name": "ACME Supplies",
  "contact_person": "Jane Doe",
  "phone": "+255700000000",
  "email": "jane@acme.example",
  "address": "Dar es Salaam",
  "tax_id": "TIN123",
  "payment_terms": "NET_30",
  "active": true,
  "version": 1,
  "created_at": "...",
  "updated_at": "..."
}
```

---

# 13. Inventory

Inventory is scoped by:

```text
merchant_id + branch_id + product_id
```

Inventory responses include `version`.

Flutter must use this version for inventory-affecting commands.

---

## 13.1 Receive Stock

```text
POST /inventory/receive
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-INV-000001
X-Expected-Version: 0
```

Use `0` for first stock receipt of a product at a branch.

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "product_id": "P001",
  "sku": "SODA-500ML",
  "quantity": 100,
  "cost_price": 50
}
```

---

## 13.2 Deduct Stock

```text
POST /inventory/deduct
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-INV-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "product_id": "P001",
  "sku": "SODA-500ML",
  "quantity": 2,
  "reason": "SALE"
}
```

---

## 13.3 Adjust Stock

```text
POST /inventory/adjust
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-INV-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "product_id": "P001",
  "sku": "SODA-500ML",
  "adjustment": -1,
  "reason": "DAMAGED_GOODS"
}
```

---

## 13.4 List Merchant Inventory

```text
GET /inventory/{merchant_id}
```

---

## 13.5 List Branch Inventory

```text
GET /inventory/{merchant_id}/branch/{branch_id}
```

---

## 13.6 Product Inventory at Branch

```text
GET /inventory/{merchant_id}/branch/{branch_id}/product/{product_id}
```

### Response Shape

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "product_id": "P001",
  "sku": "SODA-500ML",
  "quantity": 98,
  "last_cost_price": 50,
  "version": 2,
  "updated_at": "..."
}
```

---

# 14. Sales

Sales are merchant-scoped and branch-scoped.

Sale creation emits sale events.

After `SALE_COMPLETED`, the Sales Reaction Worker can:

```text
deduct inventory
create and complete payment for non-credit sales
create receivable for credit sales
```

---

## 14.1 Create Sale

```text
POST /sales
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SALE-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "payment_method": "CASH",
  "customer_id": null,
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 2,
      "unit_price": 500,
      "inventory_expected_version": 3
    }
  ]
}
```

### Supported Payment Methods

```text
CASH
MOBILE_MONEY
BANK
CARD
CREDIT
```

For `CREDIT`, `customer_id` is required.

---

## 14.2 Sales Summary

```text
GET /sales/summary/{merchant_id}
```

---

## 14.3 List Sales

```text
GET /sales/{merchant_id}
```

---

## 14.4 List Branch Sales

```text
GET /sales/{merchant_id}/branch/{branch_id}
```

---

## 14.5 Sale Detail

```text
GET /sales/{merchant_id}/{sale_id}
```

---

# 15. Purchases

Purchases are merchant-scoped and branch-scoped procurement records.

Purchases depend on:

```text
Branches
Products
Suppliers
Inventory
```

Purchase receiving emits `PURCHASE_RECEIVED`.

A purchase reaction worker receives that event and dispatches inventory receive commands.

---

## 15.1 Create Purchase

```text
POST /purchases
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "supplier_id": "SUP001",
  "supplier_invoice_ref": "INV-1001",
  "notes": "Restock drinks",
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 100,
      "unit_cost": 60
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "purchase_id": "...",
  "event_id": "...",
  "event_type": "PURCHASE_CREATED",
  "version": 1,
  "total": 6000
}
```

---

## 15.2 Receive Purchase

```text
POST /purchases/receive
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "purchase_id": "...",
  "received_by_user_id": "...",
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 100,
      "cost_price": 60,
      "inventory_expected_version": 0
    }
  ]
}
```

Use `inventory_expected_version = 0` when the destination branch has never held that product before.

---

## 15.3 Cancel Purchase

```text
POST /purchases/cancel
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000003
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "purchase_id": "...",
  "reason": "Wrong supplier invoice"
}
```

---

## 15.4 List Purchases

```text
GET /purchases/{merchant_id}
```

Optional:

```text
?status=CREATED
?status=RECEIVED
?status=CANCELLED
```

---

## 15.5 Branch Purchases

```text
GET /purchases/{merchant_id}/branch/{branch_id}
```

---

## 15.6 Supplier Purchases

```text
GET /purchases/{merchant_id}/supplier/{supplier_id}
```

---

## 15.7 Purchase Detail

```text
GET /purchases/{merchant_id}/{purchase_id}
```

---

# 16. Transfers

Transfers support two workflows:

```text
STOCK_TRANSFER
FUNDS_MOVEMENT_INTENT
```

Stock transfers move inventory between merchant branches.

Funds movement intents record non-custodial business money movement instructions.

AviaPOS does not hold funds or model wallet balances.

RailOne may later consume funds movement intents for:

```text
routing
execution continuity
provider references
settlement references
replay lineage
reconciliation
```

---

## 16.1 Stock Transfer Flow

```text
Create stock transfer
    ↓
Dispatch stock transfer
    ↓
Reaction worker deducts inventory from source branch
    ↓
Receive stock transfer
    ↓
Reaction worker receives inventory into destination branch
```

---

## 16.2 Funds Movement Intent Flow

```text
Create funds movement intent
    ↓
Optional RailOne routing/execution reference
    ↓
External rail/provider executes outside AviaPOS custody
    ↓
Confirm or fail funds movement
    ↓
Record reconciliation/provider references
```

---

## 16.3 Create Stock Transfer

```text
POST /transfers/stock
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-TRF-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "source_branch_id": "B001",
  "destination_branch_id": "B002",
  "notes": "Move drinks to branch 2",
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 20
    }
  ]
}
```

---

## 16.4 Dispatch Stock Transfer

```text
POST /transfers/stock/dispatch
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-TRF-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "transfer_id": "...",
  "dispatched_by_user_id": "...",
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 20,
      "source_inventory_expected_version": 4
    }
  ]
}
```

---

## 16.5 Receive Stock Transfer

```text
POST /transfers/stock/receive
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-TRF-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "transfer_id": "...",
  "received_by_user_id": "...",
  "items": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 20,
      "cost_price": 60,
      "destination_inventory_expected_version": 0
    }
  ]
}
```

---

## 16.6 Create Funds Movement Intent

```text
POST /transfers/funds-intent
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-FUNDS-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "source_branch_id": "B001",
  "destination_type": "SUPPLIER",
  "destination_reference": "SUP001",
  "amount": 25000,
  "currency": "TZS",
  "purpose": "Supplier payment",
  "rail_hint": "M_PESA_PAYBILL",
  "external_reference": null,
  "railone_intent_id": null
}
```

Supported `destination_type` values:

```text
BRANCH
SUPPLIER
BANK_ACCOUNT
MOBILE_MONEY_TILL
MOBILE_MONEY_PAYBILL
EXTERNAL_MERCHANT
RAILONE_ALIAS
```

This endpoint records intent only.

It does not hold funds.

It does not debit an Avia wallet.

It does not custody merchant money.

---

## 16.7 Confirm Funds Movement

```text
POST /transfers/funds/confirm
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-FUNDS-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "transfer_id": "...",
  "provider_reference": "MPESA123456",
  "external_reference": "PAYBILL-REF-001",
  "railone_intent_id": "UTT-...",
  "reconciliation_state": "CONFIRMED"
}
```

---

## 16.8 Fail Funds Movement

```text
POST /transfers/funds/fail
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-FUNDS-000003
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "transfer_id": "...",
  "reason": "Provider rejected transaction",
  "provider_reference": "MPESA123456",
  "external_reference": "PAYBILL-REF-001",
  "railone_intent_id": "UTT-..."
}
```

---

## 16.9 Cancel Transfer

```text
POST /transfers/cancel
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-TRF-000004
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "transfer_id": "...",
  "reason": "Created by mistake"
}
```

---

## 16.10 List Transfers

```text
GET /transfers/{merchant_id}
```

Optional:

```text
?transfer_type=STOCK_TRANSFER
?transfer_type=FUNDS_MOVEMENT_INTENT
?status=STOCK_CREATED
?status=STOCK_DISPATCHED
?status=STOCK_RECEIVED
?status=FUNDS_INTENT_CREATED
?status=FUNDS_CONFIRMED
?status=FUNDS_FAILED
```

---

## 16.11 Branch Transfers

```text
GET /transfers/{merchant_id}/branch/{branch_id}
```

---

## 16.12 Transfer Detail

```text
GET /transfers/{merchant_id}/{transfer_id}
```

---

# 17. Expenses

Expenses are merchant-scoped and branch-scoped.

---

## 17.1 Create Expense

```text
POST /expenses
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-EXP-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "category": "Rent",
  "description": "Shop rent",
  "amount": 50000,
  "reference": "June rent"
}
```

---

## 17.2 Approve Expense

```text
POST /expenses/approve
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-EXP-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "expense_id": "..."
}
```

---

## 17.3 Pay Expense

```text
POST /expenses/pay
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-EXP-000003
X-Expected-Version: 2
```

### Body

```json
{
  "merchant_id": "M001",
  "expense_id": "...",
  "payment_method": "CASH"
}
```

---

## 17.4 Expense Summary

```text
GET /expenses/summary/{merchant_id}
```

---

## 17.5 List Expenses

```text
GET /expenses/{merchant_id}
```

---

# 18. Payments

Payments are merchant-scoped payment records.

Payments may represent:

```text
cash payment
card payment
bank payment
mobile money payment
external merchant rail reference
sale payment reference
expense payment reference
receivable payment reference
```

Payments are records of business payment events.

Payments do not mean AviaPOS holds funds.

---

## 18.1 Create Payment

```text
POST /payments
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PAY-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "amount": 25000,
  "payment_method": "CASH",
  "reference_type": "SALE",
  "reference_id": "...",
  "notes": "Payment for sale"
}
```

---

## 18.2 Complete Payment

```text
POST /payments/complete
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PAY-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "payment_id": "..."
}
```

---

## 18.3 Fail Payment

```text
POST /payments/fail
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PAY-000003
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "payment_id": "...",
  "reason": "Provider timeout"
}
```

---

## 18.4 Cancel Payment

```text
POST /payments/cancel
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PAY-000004
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "payment_id": "...",
  "reason": "Customer cancelled"
}
```

---

## 18.5 List Payments

```text
GET /payments/{merchant_id}
```

---

## 18.6 Payment Reference Types

```text
SALE
RECEIVABLE
PAYABLE
EXPENSE
TRANSFER
RAILONE_INTENT
```


# 19. Payment Capture

Payment Capture records external provider payment evidence.

Examples:

```text
M-PESA Till payment
M-PESA Paybill payment
bank transfer reference
card provider reference
mobile money reference
manual payment confirmation


# 19. Merchant Payment Capture

AviaPOS must be able to pair with external merchant payment rails such as:

```text
M-PESA Till
M-PESA Paybill
bank transfer references
card provider references
mobile money merchant systems
other payment provider callbacks
```

Current payment capture principle:

```text
External provider receives or processes payment
    ↓
AviaPOS captures the payment event/reference
    ↓
AviaPOS links the reference to Sale, Receivable, Expense, Transfer, or RailOne intent
    ↓
AviaPOS records reconciliation state
    ↓
AviaPOS does not hold funds
```

Recommended captured fields:

```text
provider
provider_reference
external_reference
payer_reference
amount
currency
merchant_id
branch_id
reference_type
reference_id
reconciliation_state
received_at
```

This can later become a dedicated `payment_capture` module or provider adapter layer.

## Capture External Payment

POST /payment-captures

### Headers

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CAP-000001

### Body

{
  "merchant_id": "M001",
  "branch_id": "B001",
  "provider": "MPESA",
  "provider_channel": "MPESA_PAYBILL",
  "provider_reference": "RGT123456",
  "external_reference": "PAYBILL-REF-001",
  "payer_reference": "+254700000000",
  "payer_name": "John Doe",
  "amount": 2500,
  "currency": "KES",
  "payment_method": "MOBILE_MONEY",
  "reference_type": "SALE",
  "reference_id": "SALE001",
  "railone_intent_id": null,
  "raw_payload": {}
}

If reference_type and reference_id are provided, the capture is immediately MATCHED.

If not provided, the capture is stored as CAPTURED and can be matched later.

## Match Payment Capture
POST /payment-captures/match

### Headers
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CAP-000002
X-Expected-Version: 1

### Body
{
  "merchant_id": "M001",
  "capture_id": "...",
  "reference_type": "SALE",
  "reference_id": "SALE001",
  "notes": "Matched to sale after manual review"
}

## Reconcile Payment Capture
POST /payment-captures/reconcile

### Headers
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CAP-000003
X-Expected-Version: 2

### Body
{
  "merchant_id": "M001",
  "capture_id": "...",
  "reconciliation_state": "RECONCILED",
  "provider_reference": "RGT123456",
  "external_reference": "PAYBILL-REF-001",
  "railone_intent_id": null,
  "notes": "Confirmed against provider statement"
}

## Fail Payment Capture
POST /payment-captures/fail

### Headers
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CAP-000004
X-Expected-Version: 1

### Body
{
  "merchant_id": "M001",
  "capture_id": "...",
  "reason": "Provider reversed transaction",
  "provider_reference": "RGT123456"
}

## List Payment Captures
GET /payment-capture/{merchant_id}

?status=CAPTURED
?status=MATCHED
?status=RECONCILED
?status=FAILED
?provider=MPESA
?reference_type=SALE


## Branch Payment Captures
GET /payment-captures/{merchant_id}/branch/{branch_id}

## Search Payment Captures
GET /payment-captures/{merchant_id}/search?q=RGT123456

## Payment Capture Detail
GET /payment-captures/{merchant_id}/{capture_id}

### Response Shape
{
  "capture_id": "...",
  "merchant_id": "M001",
  "branch_id": "B001",
  "provider": "MPESA",
  "provider_channel": "MPESA_PAYBILL",
  "provider_reference": "RGT123456",
  "external_reference": "PAYBILL-REF-001",
  "payer_reference": "+254700000000",
  "payer_name": "John Doe",
  "amount": 2500,
  "currency": "KES",
  "payment_method": "MOBILE_MONEY",
  "reference_type": "SALE",
  "reference_id": "SALE001",
  "payment_id": null,
  "railone_intent_id": null,
  "status": "MATCHED",
  "reconciliation_state": "MATCHED",
  "reason": null,
  "notes": null,
  "raw_payload": {},
  "capture_metadata": {
    "custody_model": "NON_CUSTODIAL",
    "funds_held_by_avia": false
  },
  "version": 1,
  "received_at": "...",
  "created_at": "...",
  "updated_at": "..."
}

# 20. Receivables

Receivables represent money owed to the merchant.

Receivables are created by:

```text
credit sales
manual receivable creation
future invoices
```

Receivable responses include `version`.

---

## 20.1 Create Receivable

```text
POST /receivables
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-REC-000001
```

### Body

```json
{
  "merchant_id": "M001",
  "branch_id": "B001",
  "customer_id": "C001",
  "sale_id": "S001",
  "amount": 75000
}
```

---

## 20.2 Record Receivable Payment

```text
POST /receivables/payment
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-REC-000002
X-Expected-Version: 1
```

### Body

```json
{
  "merchant_id": "M001",
  "receivable_id": "...",
  "amount": 25000,
  "payment_method": "CASH"
}
```

---

## 20.3 Receivables Summary

```text
GET /receivables/summary/{merchant_id}
```

---

## 20.4 Open Receivables

```text
GET /receivables/{merchant_id}
```

### Response Shape

```json
[
  {
    "receivable_id": "...",
    "merchant_id": "M001",
    "branch_id": "B001",
    "customer_id": "C001",
    "sale_id": "S001",
    "amount": 75000,
    "paid_amount": 25000,
    "balance": 50000,
    "status": "OPEN",
    "version": 2,
    "created_at": "..."
  }
]
```

---

# 21. Sync

Sync is the offline-first bridge.

Flutter should maintain local queues and use Sync APIs to:

```text
register device
push local events
pull server events
track sync offsets
recover after app restart
```

---

## 21.1 Register Device

```text
POST /sync/devices/register
```

### Headers

```text
Authorization: Bearer <token>
```

### Body

```json
{
  "merchant_id": "M001",
  "device_id": "POS01",
  "branch_id": "B001",
  "device_name": "Main Counter Android",
  "platform": "ANDROID"
}
```

### Response

```json
{
  "success": true,
  "merchant_id": "M001",
  "device_id": "POS01",
  "status": "ACTIVE"
}
```

---

## 21.2 Push Offline Events

```text
POST /sync/push
```

### Headers

```text
Authorization: Bearer <token>
```

### Body

```json
{
  "merchant_id": "M001",
  "device_id": "POS01",
  "branch_id": "B001",
  "events": [
    {
      "client_event_id": "LOCAL-000001",
      "idempotency_key": "M001-POS01-LOCAL-000001",
      "command_name": "CreateExpenseCommand",
      "payload": {},
      "expected_version": null,
      "occurred_at": "2026-06-28T12:00:00Z"
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "accepted": 1,
  "results": [
    {
      "client_event_id": "LOCAL-000001",
      "status": "RECEIVED",
      "server_sync_id": 1,
      "error": null
    }
  ]
}
```

---

## 21.3 Pull Server Events

```text
GET /sync/pull/{merchant_id}?after_event_id=0&limit=100
```

### Headers

```text
Authorization: Bearer <token>
```

### Response

```json
{
  "merchant_id": "M001",
  "after_event_id": 0,
  "count": 1,
  "events": [
    {
      "id": 1,
      "event_id": "...",
      "event_type": "PRODUCT_CREATED",
      "merchant_id": "M001",
      "aggregate_id": "product:P001",
      "version": 1,
      "payload": {},
      "previous_hash": "...",
      "current_hash": "...",
      "created_at": "..."
    }
  ]
}
```

---

## 21.4 Device Sync Status

```text
GET /sync/status/{merchant_id}/{device_id}
```

---

# 22. Integrity

Integrity endpoints are admin/control endpoints.

Flutter normally does not need them for daily POS use.

---

## 22.1 Verify Merchant Chain

```text
GET /control/integrity/merchant/{merchant_id}
```

---

## 22.2 Verify Aggregate Integrity

```text
GET /control/integrity/aggregate/{merchant_id}/{aggregate_id}
```

---

# 23. Flutter Local Storage Guidance

Flutter should maintain local tables for:

```text
local_events
server_events
sync_offsets
cached_branches
cached_products
cached_customers
cached_suppliers
cached_inventory
cached_sales
cached_purchases
cached_transfers
cached_expenses
cached_payments
cached_receivables
```

---

## 23.1 Local Event Minimum Fields

```text
local_event_id
merchant_id
branch_id
device_id
command_name
payload
idempotency_key
expected_version
sync_status
created_at
synced_at
last_error
```

---

## 23.2 Recommended Sync Status Values

```text
LOCAL_PENDING
PUSHING
PUSHED
SERVER_RECEIVED
SYNCED
FAILED
CONFLICT
```

---

# 24. Recommended POS Sale Flow

```text
1. User selects active branch
2. User selects products
3. Flutter loads branch inventory row for each product
4. Flutter includes inventory_expected_version for each item
5. Flutter sends POST /sales
6. Backend records sale events
7. Sales reaction worker deducts inventory
8. Sales reaction worker creates payment or receivable
9. Flutter pulls latest events through Sync
10. Flutter refreshes local projections/cache
```

---

# 25. Recommended Purchase Flow

```text
1. User selects supplier
2. User selects branch receiving stock
3. User selects products and quantities
4. Flutter sends POST /purchases
5. Purchase remains CREATED
6. When goods arrive, Flutter loads inventory versions
7. Flutter sends POST /purchases/receive
8. Purchase reaction worker receives inventory
9. Flutter pulls latest server events
10. Local inventory cache updates
```

---

# 26. Recommended Stock Transfer Flow

```text
1. User selects source branch
2. User selects destination branch
3. User selects products and quantities
4. Flutter sends POST /transfers/stock
5. Source branch dispatches transfer
6. Flutter includes source inventory expected versions
7. Backend records TRANSFER_DISPATCHED
8. Transfer reaction worker deducts source branch inventory
9. Destination branch receives transfer
10. Flutter includes destination inventory expected versions
11. Backend records TRANSFER_RECEIVED
12. Transfer reaction worker receives destination branch inventory
```

---

# 27. Recommended Funds Movement Flow

```text
1. User chooses payment purpose
2. User chooses destination type
3. User enters amount and currency
4. User optionally selects source branch
5. Flutter sends POST /transfers/funds-intent
6. AviaPOS records non-custodial funds movement intent
7. External provider or RailOne handles execution outside AviaPOS custody
8. Backend records provider reference / RailOne intent reference
9. Funds movement is confirmed or failed
10. Flutter shows reconciliation status
```

---

# 28. RailOne Boundary

RailOne should later consume AviaPOS commercial context.

Useful AviaPOS context for RailOne:

```text
merchant_id
branch_id
supplier_id
customer_id
sale_id
purchase_id
transfer_id
payment_id
receivable_id
amount
currency
purpose
destination_type
destination_reference
external_reference
expected settlement amount
provider confirmation
reconciliation state
```

RailOne should return:

```text
utt_id
rtt_id
continuity_uid
route_id
provider_reference
settlement_reference
execution_status
replay_generation
reconciliation_state
failure_reason
```

AviaPOS records these references.

AviaPOS does not execute custody.

---

# 29. Current Launch Spine

The current merchant-onboarding backend spine is:

```text
Auth
Dashboard
Branches
Products
Customers
Suppliers
Purchases
Transfers
Sales
Inventory
Expenses
Payments
Receivables
Sync
Integrity
```

This is enough to start controlled merchant onboarding once these pass:

```text
compileall
verify_imports
legacy_import_scan
database migrations
basic endpoint smoke tests
merchant onboarding smoke test
sale-to-inventory reaction test
purchase-to-inventory reaction test
stock-transfer reaction test
funds-intent non-custodial flow test
```

---

# 30. Next Backend Modules

Recommended next modules:

```text
Payment Capture Adapters
Provider References
Reconciliation
Payables
Reports
RailOne Adapter
FX Variant
Pharma Variant
```

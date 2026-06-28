# AviaPOS Flutter API Contract

## Status

Accepted baseline for Flutter integration.

## Purpose

This document defines the active backend API surface Flutter should build against.

Flutter must not depend on:

```text
api/routes/*
app_context.py
application/*
storage/sqlite/*
core.ledger.store
modules.debts/*
legacy service files
```

Flutter should treat AviaPOS as a normal authenticated REST API.

---

# Active Runtime Surface

The active production-facing runtime currently exposes:

```text
/auth
/dashboard
/products
/sales
/inventory
/expenses
/payments
/receivables
/sync
/control/integrity
```

Deprecated or quarantined routes must not be used by Flutter.

---

# General Rules

## Authentication

All protected requests must include:

```text
Authorization: Bearer <access_token>
```

The access token is returned by:

```text
POST /auth/login
```

---

## Merchant Scope

Most requests include:

```json
{
  "merchant_id": "M001"
}
```

The backend validates this against the authenticated JWT merchant scope.

Flutter must not allow a user to manually change `merchant_id`.

Use the `merchant_id` returned by:

```text
GET /auth/me
```

---

## Branch Scope

Branch-scoped domains include:

```text
Sales
Inventory
Receivables
Expenses
Dashboard branch view
```

Flutter should keep the active branch in local app state after login.

---

## Idempotency

All command/write endpoints must include:

```text
Idempotency-Key: <client-generated-key>
```

Recommended Flutter format:

```text
<merchant_id>-<device_id>-<domain>-<local_sequence>
```

Examples:

```text
M001-POS01-SALE-000001
M001-POS01-PROD-000001
M001-POS01-INV-000001
```

Idempotency protects against duplicate submissions caused by:

```text
offline retry
network timeout
double tap
app restart
sync replay
```

---

## Optimistic Concurrency

State-changing update endpoints require:

```text
X-Expected-Version: <current_known_version>
```

Flutter gets `version` from read endpoints.

If the backend returns `409 Conflict`, Flutter should refresh the latest item and ask the user to retry.

If the backend returns `428 Precondition Required`, Flutter forgot to send `X-Expected-Version`.

---

## Standard Error Behavior

Common errors:

```text
400 Bad Request
```

Invalid request body or business rule violation.

```text
401 Unauthorized
```

Missing, invalid, or expired token.

```text
403 Forbidden
```

Authenticated user is not allowed to access the merchant/resource.

```text
404 Not Found
```

Requested resource does not exist.

```text
409 Conflict
```

Idempotency conflict, command already in progress, or optimistic concurrency failure.

```text
428 Precondition Required
```

`X-Expected-Version` is required but missing.

---

# Auth

## Bootstrap Owner

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

## Login

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

## Current User

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

## Create User

```text
POST /auth/users
```

Only `OWNER` and `MANAGER` users can create users.

Managers cannot create owners or other managers.

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

# Dashboard

Dashboard is read-only.

It reads PostgreSQL projection tables.

It does not:

```text
write events
dispatch commands
publish Redis messages
replay the event store
```

---

## Merchant Dashboard

```text
GET /dashboard/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

### Response

```json
{
  "merchant_id": "M001",
  "branch_id": null,
  "sales": {
    "total_sales_value": 0,
    "completed_count": 0,
    "total_count": 0,
    "average_sale_value": 0,
    "recent_sales": []
  },
  "inventory": {
    "tracked_items": 0,
    "total_units": 0,
    "low_stock_count": 0,
    "negative_stock_count": 0,
    "low_stock_items": []
  },
  "cashflow": {
    "completed_payments": 0,
    "paid_expenses": 0,
    "net_cash_indicator": 0
  },
  "receivables": {
    "total_original": 0,
    "total_paid": 0,
    "outstanding": 0,
    "open_count": 0,
    "settled_count": 0,
    "count": 0
  },
  "expenses": {
    "total_expenses": 0,
    "paid_expenses": 0,
    "pending_count": 0,
    "approved_count": 0,
    "paid_count": 0,
    "count": 0
  },
  "payments": {
    "completed_payments": 0,
    "pending_count": 0,
    "completed_count": 0,
    "failed_count": 0,
    "cancelled_count": 0,
    "count": 0
  },
  "warnings": []
}
```

---

## Branch Dashboard

```text
GET /dashboard/{merchant_id}/branch/{branch_id}
```

### Headers

```text
Authorization: Bearer <token>
```

This returns the same shape as the merchant dashboard, but branch-scoped where supported.

Currently branch-scoped:

```text
sales
inventory
expenses
receivables
```

Currently merchant-level:

```text
payments
```

---

# Products

Products are merchant-scoped reference data used by Sales and Inventory.

Product responses include `version`.

Flutter must use `version` as `X-Expected-Version` when updating or deactivating products.

---

## Create Product

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

## Update Product

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

### Response

```json
{
  "success": true,
  "product_id": "...",
  "event_id": "...",
  "event_type": "PRODUCT_UPDATED",
  "version": 2
}
```

---

## Deactivate Product

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

### Response

```json
{
  "success": true,
  "product_id": "...",
  "event_id": "...",
  "event_type": "PRODUCT_UPDATED",
  "version": 3,
  "active": false
}
```

---

## List Products

```text
GET /products/{merchant_id}
```

Optional query:

```text
?include_inactive=true
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Search Products

```text
GET /products/{merchant_id}/search?q=soda
```

Optional query:

```text
&include_inactive=true
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Product by SKU

```text
GET /products/{merchant_id}/sku/{sku}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Product Detail

```text
GET /products/{merchant_id}/{product_id}
```

### Headers

```text
Authorization: Bearer <token>
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


# Customers

Customers are merchant-scoped reference data used by Sales and Receivables.

Customer responses include `version`.

Flutter must use this `version` as `X-Expected-Version` when updating or deactivating customers.

---

## Create Customer

```text
POST /customers

# Customers

Customers are merchant-scoped reference data used by Sales and Receivables.

Customer responses include `version`.

Flutter must use this `version` as `X-Expected-Version` when updating or deactivating customers.

---

## Create Customer

```text
POST /customers


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


{
  "success": true,
  "customer_id": "...",
  "event_id": "...",
  "event_type": "CUSTOMER_CREATED",
  "version": 1
}

PATCH /customers

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000002
X-Expected-Version: 1

{
  "merchant_id": "M001",
  "customer_id": "...",
  "phone": "+255711111111",
  "credit_limit": 100000
}

POST /customers/deactivate

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000003
X-Expected-Version: 2

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-CUST-000003
X-Expected-Version: 2

{
  "merchant_id": "M001",
  "customer_id": "...",
  "reason": "Duplicate account"
}

GET /customers/{merchant_id}
?include_inactive=true

GET /customers/{merchant_id}/search?q=john
&include_inactive=true

GET /customers/{merchant_id}/{customer_id}

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
---

# Sales

Sales are merchant-scoped and branch-scoped.

Sale creation emits sale events.

After `SALE_COMPLETED`, the Sales Reaction Worker automatically:

```text
deducts inventory
creates and completes a payment for non-credit sales
creates a receivable for credit sales
```

Sales does not directly call Inventory, Payments, or Receivables.

---

## Create Sale

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

### Response

```json
{
  "success": true,
  "sale_id": "...",
  "total": 1000,
  "payment_method": "CASH",
  "event_id": "...",
  "event_type": "SALE_COMPLETED",
  "version": 3
}
```

---

## Payment Methods

Supported sale payment methods:

```text
CASH
MOBILE_MONEY
BANK
CARD
CREDIT
```

For `CREDIT`, `customer_id` is required.

---

## Inventory Version Rule

Each sale item must include:

```text
inventory_expected_version
```

Flutter gets this from:

```text
GET /inventory/{merchant_id}/branch/{branch_id}/product/{product_id}
```

If inventory changes before the sale reaction deducts stock, the inventory deduction command may fail with a concurrency conflict.

---

## Sales Summary

```text
GET /sales/summary/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## List Sales

```text
GET /sales/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## List Branch Sales

```text
GET /sales/{merchant_id}/branch/{branch_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Sale Detail

```text
GET /sales/{merchant_id}/{sale_id}
```

### Headers

```text
Authorization: Bearer <token>
```

### Response Shape

```json
{
  "sale_id": "...",
  "merchant_id": "M001",
  "branch_id": "B001",
  "customer_id": null,
  "payment_method": "CASH",
  "total": 1000,
  "status": "COMPLETED",
  "lines": [
    {
      "product_id": "P001",
      "sku": "SODA-500ML",
      "quantity": 2,
      "unit_price": 500,
      "line_total": 1000
    }
  ],
  "version": 3,
  "created_at": "...",
  "updated_at": "..."
}
```
# Suppliers

Suppliers are merchant-scoped reference data used by Purchases.

Supplier responses include `version`.

Flutter must use this `version` as `X-Expected-Version` when updating or deactivating suppliers.

---

## Create Supplier

```text
POST /suppliers

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000001

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

{
  "success": true,
  "supplier_id": "...",
  "event_id": "...",
  "event_type": "SUPPLIER_CREATED",
  "version": 1
}

PATCH /suppliers

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000002
X-Expected-Version: 1

{
  "merchant_id": "M001",
  "supplier_id": "...",
  "payment_terms": "NET_14"
}

POST /suppliers/deactivate
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-SUP-000003
X-Expected-Version: 2

{
  "merchant_id": "M001",
  "supplier_id": "...",
  "reason": "No longer active"
}

GET /suppliers/{merchant_id}
?include_inactive=true

GET /suppliers/{merchant_id}/search?q=acme

GET /suppliers/{merchant_id}/{supplier_id}
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


# Purchases

Purchases are merchant-scoped and branch-scoped procurement records.

Purchases depend on:

```text
Branches
Products
Suppliers
Inventory

# Purchases

Purchases are merchant-scoped and branch-scoped procurement records.

Purchases depend on:

```text
Branches
Products
Suppliers
Inventory

POST /purchases

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000001

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

{
  "success": true,
  "purchase_id": "...",
  "event_id": "...",
  "event_type": "PURCHASE_CREATED",
  "version": 1,
  "total": 6000
}

POST /purchases/receive

Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000002
X-Expected-Version: 1

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
inventory_expected_version comes from the current inventory row for: 
merchant_id + branch_id + product_id
Use 0 if the product has never existed in that branch inventory before.

POST /purchases/cancel
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-PUR-000003
X-Expected-Version: 1

{
  "merchant_id": "M001",
  "purchase_id": "...",
  "reason": "Wrong supplier invoice"
}

GET /purchases/{merchant_id}
?status=CREATED
?status=RECEIVED
?status=CANCELLED

GET /purchases/{merchant_id}/branch/{branch_id} 

GET /purchases/{merchant_id}/supplier/{supplier_id}

GET /purchases/{merchant_id}/{purchase_id}



# Inventory

Inventory is scoped by:

```text
merchant_id + branch_id + product_id
```

Inventory responses include `version`.

Flutter must use this `version` as `X-Expected-Version` for future inventory writes.

---

## Receive Stock

```text
POST /inventory/receive
```

### Headers

```text
Authorization: Bearer <token>
Idempotency-Key: M001-POS01-INV-000001
X-Expected-Version: 0
```

Use version `0` for first stock receipt of a product at a branch.

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

### Response

```json
{
  "success": true,
  "aggregate_id": "inventory:B001:P001",
  "event_id": "...",
  "event_type": "INVENTORY_RECEIVED",
  "version": 1
}
```

---

## Deduct Stock

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

### Response

```json
{
  "success": true,
  "aggregate_id": "inventory:B001:P001",
  "event_id": "...",
  "event_type": "INVENTORY_DEDUCTED",
  "version": 2,
  "remaining_stock": 98
}
```

---

## Adjust Stock

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

### Response

```json
{
  "success": true,
  "aggregate_id": "inventory:B001:P001",
  "event_id": "...",
  "event_type": "INVENTORY_ADJUSTED",
  "version": 3,
  "quantity": 97
}
```

---

## List Merchant Inventory

```text
GET /inventory/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## List Branch Inventory

```text
GET /inventory/{merchant_id}/branch/{branch_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Get Product Inventory at Branch

```text
GET /inventory/{merchant_id}/branch/{branch_id}/product/{product_id}
```

### Headers

```text
Authorization: Bearer <token>
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

# Expenses

Expenses are merchant-scoped and branch-scoped.

Expense writes use:

```text
Command Bus
UnitOfWork
Event Store
Outbox
Idempotency
Optimistic Concurrency
```

---

## Create Expense

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

### Response

```json
{
  "success": true,
  "expense_id": "...",
  "event_id": "...",
  "event_type": "EXPENSE_CREATED",
  "version": 1
}
```

---

## Approve Expense

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

## Pay Expense

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

## Expense Summary

```text
GET /expenses/summary/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## List Expenses

```text
GET /expenses/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

# Payments

Payments are merchant-scoped.

Payment writes use:

```text
Command Bus
UnitOfWork
Event Store
Outbox
Idempotency
Optimistic Concurrency
```

---

## Create Payment

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

### Response

```json
{
  "success": true,
  "payment_id": "...",
  "event_id": "...",
  "event_type": "PAYMENT_CREATED",
  "version": 1
}
```

---

## Complete Payment

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

## Fail Payment

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

## Cancel Payment

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

## List Payments

```text
GET /payments/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

### Payment Reference Types

Supported `reference_type` values:

```text
SALE
RECEIVABLE
PAYABLE
EXPENSE
TRANSFER
RAILONE_INTENT
```

---

# Receivables

Receivables represent money owed to the merchant.

Receivables are created for customer credit sales or manual receivable records.

Receivable responses include `version`.

Flutter must use this `version` when recording payments.

---

## Create Receivable

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

### Response

```json
{
  "success": true,
  "receivable_id": "...",
  "event_id": "...",
  "event_type": "RECEIVABLE_CREATED",
  "version": 1
}
```

---

## Record Receivable Payment

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

### Response

```json
{
  "success": true,
  "receivable_id": "...",
  "event_id": "...",
  "event_type": "RECEIVABLE_PAYMENT_RECORDED",
  "version": 2
}
```

---

## Receivables Summary

```text
GET /receivables/summary/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Open Receivables

```text
GET /receivables/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
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

# Sync

Sync is the offline-first bridge.

Flutter should maintain local queues and use Sync APIs to register devices, push client-side events, and pull server events.

The current Sync API records inbound client envelopes and exposes server event pull.

It does not yet execute all pushed commands automatically.

---

## Register Device

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

## Push Offline Events

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

## Pull Server Events

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

## Device Sync Status

```text
GET /sync/status/{merchant_id}/{device_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

# Integrity

Integrity endpoints are control endpoints used to verify hash-chain/event integrity.

Flutter normally does not need these for daily POS operation.

Admin/internal tooling may use them.

---

## Verify Merchant Chain

```text
GET /control/integrity/merchant/{merchant_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

## Verify Aggregate Integrity

```text
GET /control/integrity/aggregate/{merchant_id}/{aggregate_id}
```

### Headers

```text
Authorization: Bearer <token>
```

---

# Flutter Local Storage Guidance

Flutter should maintain local tables for:

```text
local_events
server_events
sync_offsets
cached_products
cached_inventory
cached_customers
cached_sales
cached_expenses
cached_payments
cached_receivables
```

---

## Local Event Minimum Fields

Each local event should store:

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

## Sync Status Values

Recommended local sync statuses:

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

# Recommended Flutter Startup Flow

```text
1. Open app
2. Load saved token
3. GET /auth/me
4. Load merchant_id, role, branch_id
5. Register or refresh device with /sync/devices/register
6. Pull server events with /sync/pull/{merchant_id}
7. Load dashboard with /dashboard/{merchant_id}
8. Load cached Products and Inventory for active branch
```

---

# Recommended Sale Flow

```text
1. User selects products
2. Flutter loads inventory row for each product at active branch
3. Flutter includes inventory_expected_version for each sale item
4. Flutter sends POST /sales
5. Backend records sale events
6. Sales reaction worker deducts inventory
7. Sales reaction worker creates payment or receivable
8. Flutter pulls latest events through /sync/pull
9. Flutter updates local cache
```

---

# Deprecated Routes

Flutter must not call:

```text
/debts
api/routes/*
```

Debt is deprecated in favor of:

```text
Receivables
Payables
```

The old `api/routes` folder belongs to the legacy SQLite/application-service path and is not part of the Flutter contract.

---

# Active Launch Spine

The current Flutter-ready launch spine is:

```text
Auth
Dashboard
Products
Sales
Inventory
Expenses
Payments
Receivables
Sync
Integrity
```

The next backend migrations should focus on:

```text
Customers
Branches
Suppliers
Purchases
Transfers
Payables
```

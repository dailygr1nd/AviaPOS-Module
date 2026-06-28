# AviaPOS Backend Engineering Guidelines

## Status

Accepted.

## Purpose

This document defines the backend rules for AviaPOS.

The goal is to prevent architectural drift, module bloat, duplicated services, and ERP-style feature creep.

AviaPOS is a Merchant Operating System, not a generic ERP.

---

## Core Product Scope

AviaPOS focuses on the smallest set of merchant primitives needed to operate an SME:

1. Sales
2. Inventory
3. Expenses
4. Receivables
5. Payables
6. Payments

Any new module must directly support one of these domains.

---

## Required Write Flow

All write operations must follow this flow:

```text
API Router
    ↓
Command
    ↓
Command Bus
    ↓
Command Handler
    ↓
Aggregate / Domain Rule
    ↓
Event Factory
    ↓
Event Store
    ↓
Redis Stream
    ↓
Projection Worker
    ↓
Projection Table
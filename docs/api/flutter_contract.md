# AviaPOS Flutter API Contract

## Status

Accepted for Flutter integration baseline.

## Purpose

This document defines the backend API surface Flutter should build against.

Flutter must not depend on legacy routes, SQLite internals, event-store internals, Redis internals, or projection worker behavior.

Flutter should treat AviaPOS as a normal REST API.

---

## Authentication

### Bootstrap Owner

```text
POST /auth/bootstrap-owner
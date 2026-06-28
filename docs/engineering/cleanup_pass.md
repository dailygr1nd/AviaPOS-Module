# Compile and Import Cleanup Pass

## Status

Accepted.

## Purpose

This pass removes broken legacy imports and freezes the active backend import surface.

The current production path is:

```text
FastAPI
    ↓
modules/*/api.py
    ↓
Command Bus
    ↓
UnitOfWork
    ↓
PostgreSQL Event Store + Outbox
    ↓
Redis Streams
    ↓
Projection Workers / Reaction Workers
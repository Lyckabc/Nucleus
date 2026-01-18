# Nucleus

**Nucleus** is the central database management service of the system.
Inspired by the biological cell nucleus, it acts as the single source of truth,
governing how data is stored, structured, and maintained across all backends.

Nucleus provides a stable and consistent foundation for data persistence,
schema evolution, and integrity, enabling other services to focus on
processing, signaling, and orchestration.

---

## Concept

**Biological Analogy:** Cell Nucleus  
In biology, the nucleus stores genetic information and regulates cellular activity.
Likewise, Nucleus stores core data and enforces rules that keep the system coherent
and reliable.

---

## Responsibilities

- Centralized data storage and persistence
- Schema definition and migration management
- Data integrity and consistency enforcement
- Transaction and concurrency control
- Backup, restore, and recovery coordination
- Providing a single source of truth for the system

---

## Non-Goals

- Business logic processing (handled by Metaflow)
- Event propagation or signaling (handled by Synapse)
- Authentication or authorization logic (handled by LymphHub)
- Data ingestion or classification (handled by Taxon)

---

## Architecture Position


# system-patterns

**Common design patterns for building robust systems**

---

## Overview

This branch catalogs 10 battle-tested design patterns for solving common problems in software architecture. Each pattern includes problem/solution, usage guidelines, and examples.

## Pattern Categories

### Data Access
- **Repository** - Abstract data access

### Resilience
- **Circuit Breaker** - Prevent cascading failures
- **Bulkhead** - Isolate resources

### Data Management
- **Event Sourcing** - Store events, not state
- **CQRS** - Separate read/write models
- **Cache-Aside** - Application-managed caching

### Microservices
- **Saga** - Distributed transactions
- **Backend for Frontend (BFF)** - Tailored APIs
- **Sidecar** - Extend without changing code

### Migration
- **Strangler Fig** - Incremental replacement

---

## Patterns

### 1. Repository Pattern
**Problem:** Direct database access scattered throughout codebase  
**Solution:** Single source of truth for data operations  

**When to use:**
- Need to swap data sources
- Want to test without database
- Multiple data access points

**Example:**
```
IUserRepository interface
  ↓
UserRepository implementation
  ↓
Service depends on interface
```

---

### 2. Circuit Breaker Pattern
**Problem:** Failing service causes cascading failures  
**Solution:** Detect failures, short-circuit failing service  

**States:**
- Closed (normal operation)
- Open (failing, rejecting requests)
- Half-Open (testing recovery)

**When to use:**
- Calling external services
- Microservice architecture
- Need to fail fast

---

### 3. Event Sourcing Pattern
**Problem:** Lost history of state changes  
**Solution:** Store events instead of state, rebuild from events  

**Components:**
- Event Store (append-only log)
- Event Stream
- Projections/Views
- Snapshots (performance)

**When to use:**
- Need complete audit trail
- Want to replay events
- Temporal queries required

---

### 4. CQRS Pattern
**Problem:** Same model for reads/writes leads to complexity  
**Solution:** Separate command (write) and query (read) models  

**When to use:**
- Read/write patterns differ
- Scale reads independently
- Complex write business logic
- Different consistency needs

**Components:**
- Command Side: Writes, business rules
- Query Side: Optimized reads, denormalized
- Sync: Events or CDC

---

### 5. Saga Pattern
**Problem:** No ACID transactions across microservices  
**Solution:** Sequence of local transactions with compensating actions  

**Types:**
- **Choreography:** Each service reacts to events
- **Orchestration:** Central coordinator

**When to use:**
- Multi-service transactions
- Eventual consistency acceptable
- Can define compensations

**Example:** Order saga
```
Reserve inventory → Charge payment → Ship order
     ↓ (fail)          ↓ (fail)         ↓ (fail)
Unreserve         Refund           Cancel ship
```

---

### 6. Strangler Fig Pattern
**Problem:** Legacy system needs replacement, can't stop business  
**Solution:** Incrementally replace, route traffic to new system  

**Phases:**
1. Setup routing/facade
2. Implement new features in new system
3. Migrate existing features incrementally
4. Decommission old system

**When to use:**
- Legacy modernization
- Cannot afford downtime
- Risk mitigation needed

---

### 7. Backend for Frontend (BFF) Pattern
**Problem:** Generic API doesn't fit all frontend needs  
**Solution:** Separate backend for each frontend type  

**When to use:**
- Multiple frontend types
- Different data requirements
- Optimize for client constraints

**Examples:**
- Mobile BFF: Smaller payloads, offline
- Web BFF: Rich data, pagination
- IoT BFF: Minimal data, batch updates

---

### 8. Bulkhead Pattern
**Problem:** One failing component consumes all resources  
**Solution:** Partition resources to isolate failures  

**When to use:**
- Shared resource pools
- Multi-tenant systems
- Need fault isolation

**Examples:**
- Separate thread pools per service
- Connection pool per client
- Rate limits per tenant

**Analogy:** Ship bulkheads - one floods, ship stays afloat

---

### 9. Sidecar Pattern
**Problem:** Cross-cutting concerns duplicate across services  
**Solution:** Deploy helper container alongside main service  

**When to use:**
- Logging, monitoring, config
- Service mesh
- Language-agnostic features

**Common sidecars:**
- Envoy proxy
- Log forwarder
- Config watcher
- Metrics collector

---

### 10. Cache-Aside Pattern
**Problem:** Database queries too slow  
**Solution:** Check cache first, load from DB on miss  

**Flow:**
```
1. Check cache
2. If miss → load from DB
3. Populate cache
4. Return data
```

**When to use:**
- Read-heavy workloads
- Expensive queries
- Tolerate slight staleness

**Considerations:** TTL, eviction policy, invalidation strategy

---

## Pattern Selection Guide

**Need resilience?**
→ Circuit Breaker, Bulkhead

**Managing data?**
→ Repository, Event Sourcing, CQRS, Cache-Aside

**Building microservices?**
→ Saga, BFF, Sidecar

**Migrating legacy?**
→ Strangler Fig

**Scaling reads?**
→ CQRS, Cache-Aside

**Distributed transactions?**
→ Saga

---

## Combining Patterns

Patterns often work together:

**Microservice with resilience:**
- Circuit Breaker (prevent cascades)
- Bulkhead (isolate resources)
- Sidecar (logging/monitoring)

**Event-driven architecture:**
- Event Sourcing (store events)
- CQRS (separate read/write)
- Saga (distributed transactions)

**API optimization:**
- BFF (tailor to clients)
- Cache-Aside (speed up reads)
- Circuit Breaker (handle failures)

---

## Anti-Patterns to Avoid

- **Distributed Monolith** - Microservices that depend on each other
- **God Service** - One service does everything
- **Chatty APIs** - Too many round trips
- **Shared Database** - Microservices sharing database
- **Premature Optimization** - Using patterns before needed

---

## Contributing

Know a pattern?

```bash
python kt.py add doc "Pattern Name" --branch system-patterns \
  --reasoning "Problem and solution description" \
  --tags pattern,category
```

Include:
- Pattern name
- Problem it solves
- Solution approach
- When to use it
- Examples
- Benefits and tradeoffs

---

**Status:** 10 production-ready patterns  
**Last updated:** 2026-03-09

#!/usr/bin/env python3
"""
Create system-patterns branch with common design patterns
"""

import json
from pathlib import Path
from datetime import datetime

# Create branch structure
branch_dir = Path("branches/system-patterns")
knowledge_dir = branch_dir / "knowledge"
knowledge_dir.mkdir(parents=True, exist_ok=True)

# Pattern definitions
patterns = [
    {
        "id": "0",
        "type": "init",
        "message": "Design Patterns - Common solutions to recurring problems",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tags": ["patterns", "system", "init"]
    },
    {
        "id": "1",
        "type": "documentation",
        "message": "Repository Pattern",
        "reasoning": "Abstracts data access, enables testing, centralizes data logic",
        "tags": ["pattern", "data-access", "architecture"],
        "content": {
            "pattern_name": "Repository",
            "category": "Data Access",
            "problem": "Direct database access scattered throughout codebase",
            "solution": "Single source of truth for data operations",
            "when_to_use": [
                "Need to swap data sources",
                "Want to test business logic without database",
                "Multiple data access points",
                "Complex queries need centralization"
            ],
            "example": {
                "interface": "IUserRepository with get(), save(), delete()",
                "implementation": "UserRepository implements IUserRepository",
                "usage": "Service depends on IUserRepository, not database"
            }
        }
    },
    {
        "id": "2",
        "type": "documentation",
        "message": "Circuit Breaker Pattern",
        "reasoning": "Prevents cascading failures in distributed systems",
        "tags": ["pattern", "resilience", "microservices"],
        "content": {
            "pattern_name": "Circuit Breaker",
            "category": "Resilience",
            "problem": "Failing service causes timeout waits and cascading failures",
            "solution": "Detect failures and short-circuit requests to failing service",
            "states": ["Closed (normal)", "Open (failing)", "Half-Open (testing)"],
            "when_to_use": [
                "Calling external services",
                "Microservice architecture",
                "Need to prevent cascade failures",
                "Want to fail fast"
            ],
            "thresholds": {
                "failure_count": "e.g., 5 failures",
                "timeout": "e.g., 30 seconds",
                "retry_after": "e.g., 60 seconds"
            }
        }
    },
    {
        "id": "3",
        "type": "documentation",
        "message": "Event Sourcing Pattern",
        "reasoning": "Capture all changes as sequence of events, enables audit trail and time travel",
        "tags": ["pattern", "data", "architecture"],
        "content": {
            "pattern_name": "Event Sourcing",
            "category": "Data Management",
            "problem": "Lost history of state changes, difficult audit trail",
            "solution": "Store events instead of current state, rebuild state from events",
            "when_to_use": [
                "Need complete audit trail",
                "Want to replay events",
                "Temporal queries needed",
                "Complex business logic with state changes"
            ],
            "components": ["Event Store", "Event Stream", "Projections/Views", "Snapshots"],
            "benefits": ["Complete history", "Time travel", "Event replay", "Audit trail"],
            "challenges": ["Eventual consistency", "Schema evolution", "Snapshot management"]
        }
    },
    {
        "id": "4",
        "type": "documentation",
        "message": "CQRS Pattern",
        "reasoning": "Separate read and write models for scalability and clarity",
        "tags": ["pattern", "architecture", "scalability"],
        "content": {
            "pattern_name": "CQRS (Command Query Responsibility Segregation)",
            "category": "Architecture",
            "problem": "Same model for reads and writes leads to complexity",
            "solution": "Separate models: Commands (write) and Queries (read)",
            "when_to_use": [
                "Read and write patterns differ significantly",
                "Need to scale reads independently",
                "Complex business logic on writes",
                "Different consistency requirements"
            ],
            "components": {
                "Command Side": "Handles writes, enforces business rules",
                "Query Side": "Optimized read models, denormalized",
                "Sync Mechanism": "Events, CDC, or direct sync"
            }
        }
    },
    {
        "id": "5",
        "type": "documentation",
        "message": "Saga Pattern",
        "reasoning": "Manage distributed transactions across microservices",
        "tags": ["pattern", "microservices", "transactions"],
        "content": {
            "pattern_name": "Saga",
            "category": "Distributed Transactions",
            "problem": "No ACID transactions across microservices",
            "solution": "Sequence of local transactions with compensating actions",
            "types": {
                "Choreography": "Each service publishes events, others react",
                "Orchestration": "Central coordinator directs the saga"
            },
            "when_to_use": [
                "Multi-service transactions",
                "Need eventual consistency",
                "Can define compensating actions",
                "Business process spans services"
            ],
            "example": "Order saga: Reserve inventory → Charge payment → Ship order (with compensations)"
        }
    },
    {
        "id": "6",
        "type": "documentation",
        "message": "Strangler Fig Pattern",
        "reasoning": "Gradually replace legacy system without big-bang rewrite",
        "tags": ["pattern", "migration", "legacy"],
        "content": {
            "pattern_name": "Strangler Fig",
            "category": "Migration",
            "problem": "Legacy system needs replacement but can't stop business",
            "solution": "Incrementally replace functionality, routing traffic to new system",
            "phases": [
                "Phase 1: Setup routing/facade",
                "Phase 2: Implement new features in new system",
                "Phase 3: Migrate existing features incrementally",
                "Phase 4: Decommission old system"
            ],
            "when_to_use": [
                "Legacy system modernization",
                "Cannot afford downtime",
                "Risk mitigation needed",
                "Incremental value delivery"
            ]
        }
    },
    {
        "id": "7",
        "type": "documentation",
        "message": "Backend for Frontend (BFF) Pattern",
        "reasoning": "Tailor backend APIs to specific frontend needs",
        "tags": ["pattern", "api", "frontend"],
        "content": {
            "pattern_name": "Backend for Frontend (BFF)",
            "category": "API Design",
            "problem": "Generic API doesn't fit mobile, web, and desktop needs",
            "solution": "Create separate backend layer for each frontend type",
            "when_to_use": [
                "Multiple frontend types (web, mobile, desktop)",
                "Different data requirements per frontend",
                "Need to optimize for client constraints",
                "Want to isolate frontend-specific logic"
            ],
            "examples": [
                "Mobile BFF: Optimized payloads, offline support",
                "Web BFF: Rich data, pagination",
                "IoT BFF: Minimal data, batch updates"
            ]
        }
    },
    {
        "id": "8",
        "type": "documentation",
        "message": "Bulkhead Pattern",
        "reasoning": "Isolate resources to prevent total system failure",
        "tags": ["pattern", "resilience", "isolation"],
        "content": {
            "pattern_name": "Bulkhead",
            "category": "Resilience",
            "problem": "One failing component consumes all resources",
            "solution": "Partition resources so failure is isolated",
            "when_to_use": [
                "Shared resource pools",
                "Multi-tenant systems",
                "Need fault isolation",
                "Prevent cascade failures"
            ],
            "examples": [
                "Separate thread pools per service",
                "Connection pool per client",
                "Rate limits per tenant"
            ],
            "analogy": "Ship bulkheads: one compartment floods, ship stays afloat"
        }
    },
    {
        "id": "9",
        "type": "documentation",
        "message": "Sidecar Pattern",
        "reasoning": "Extend application functionality without changing code",
        "tags": ["pattern", "microservices", "deployment"],
        "content": {
            "pattern_name": "Sidecar",
            "category": "Deployment",
            "problem": "Cross-cutting concerns duplicate across services",
            "solution": "Deploy helper container alongside main service",
            "when_to_use": [
                "Logging, monitoring, configuration",
                "Service mesh components",
                "Proxy/load balancing",
                "Multi-language support"
            ],
            "common_sidecars": [
                "Envoy proxy",
                "Log forwarder",
                "Config watcher",
                "Metrics collector"
            ],
            "benefits": ["Language agnostic", "Isolation", "Independent updates"]
        }
    },
    {
        "id": "10",
        "type": "documentation",
        "message": "Cache-Aside Pattern",
        "reasoning": "Application manages cache, reads from cache first",
        "tags": ["pattern", "caching", "performance"],
        "content": {
            "pattern_name": "Cache-Aside",
            "category": "Caching",
            "problem": "Database queries too slow for common reads",
            "solution": "Check cache first, load from DB on miss, populate cache",
            "flow": [
                "1. Check cache for data",
                "2. If miss, load from database",
                "3. Populate cache with result",
                "4. Return data"
            ],
            "when_to_use": [
                "Read-heavy workloads",
                "Expensive queries",
                "Tolerate slight staleness",
                "Application controls caching logic"
            ],
            "considerations": ["TTL strategy", "Eviction policy", "Cache invalidation"]
        }
    }
]

# Write nodes
tree_file = knowledge_dir / "tree.jsonl"
with open(tree_file, 'w', encoding='utf-8') as f:
    for node in patterns:
        f.write(json.dumps(node) + '\n')

# Create README
readme = branch_dir / "README.md"
readme_content = """# system-patterns

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
python kt.py add doc "Pattern Name" --branch system-patterns \\
  --reasoning "Problem and solution description" \\
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
"""

with open(readme, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("[OK] Created system-patterns branch")
print(f"     Location: {branch_dir}")
print(f"     Patterns: {len(patterns)}")
print(f"     README: {readme}")

---
watermark: "EduGPT KZ Educational AI - Adilet Kuralbek © 2025"
copyright: "Copyright © 2025 Adilet Kuralbek. All rights reserved."
license: "Proprietary software - Commercial use only"
contact: "Contact: adilet.kuralbek@email.com"
---

# 🏗️ Architecture Documentation

**Version:** 2.0 (PHASE 3)  
**Last updated:** 10 октября 2025

---

## 📊 System Overview

```mermaid
graph TB
    subgraph "User Layer"
        TG[Telegram Users]
        WEB[Web Users]
    end
    
    subgraph "Bot Layer"
        TGBOT[Telegram Bot<br/>aiogram 3.x]
        WEBAPP[Web Widget<br/>React]
    end
    
    subgraph "Backend Layer"
        API[FastAPI Backend<br/>REST + WebSocket]
        LLM[LLM Router<br/>GPT-4]
        FAQ[FAQ Service<br/>PostgreSQL]
        CACHE[Cache Service<br/>Redis]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>+pgvector)]
        RD[(Redis<br/>Cache + FSM)]
        OPENAI[OpenAI API<br/>Embeddings + Chat]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
        LOGS[Logs]
    end
    
    TG --> TGBOT
    WEB --> WEBAPP
    
    TGBOT --> API
    WEBAPP --> API
    
    API --> LLM
    API --> FAQ
    API --> CACHE
    
    LLM --> OPENAI
    FAQ --> PG
    CACHE --> RD
    
    API --> PROM
    API --> LOGS
    PROM --> GRAF
    
    style TG fill:#e1f5ff
    style TGBOT fill:#b3e5fc
    style API fill:#81d4fa
    style PG fill:#4fc3f7
    style OPENAI fill:#29b6f6
```

---

## 🔄 Request Flow

```mermaid
sequenceDiagram
    actor User
    participant TG as Telegram Bot
    participant API as Backend API
    participant Cache as Redis Cache
    participant LLM as LLM Router
    participant DB as PostgreSQL
    participant OpenAI as OpenAI API
    
    User->>TG: "Как поступить?"
    
    TG->>API: POST /api/chat
    
    API->>Cache: GET faq:all:ru
    
    alt Cache Hit (85% cases)
        Cache-->>API: FAQ data (5-10ms)
    else Cache Miss (15% cases)
        API->>DB: SELECT FAQ items
        DB-->>API: FAQ data (150ms)
        API->>Cache: SET faq:all:ru
    end
    
    API->>LLM: process_query()
    
    LLM->>DB: pgvector search
    Note over LLM,DB: SELECT ... ORDER BY<br/>embedding <=> query
    DB-->>LLM: Top-10 matches (250ms)
    
    LLM->>OpenAI: GPT-4 completion
    Note over LLM,OpenAI: With FAQ context
    OpenAI-->>LLM: Answer (1-2s)
    
    LLM-->>API: BotResponse
    API-->>TG: JSON response
    TG-->>User: Answer
    
    Note over User,TG: Total: 2-3s ✅
```

---

## 🏗️ Component Architecture

```mermaid
graph LR
    subgraph "Presentation Layer"
        UI1[Telegram Bot]
        UI2[Web Interface]
    end
    
    subgraph "Application Layer"
        BL1[LLM Router]
        BL2[FAQ Service]
        BL3[Guardrails]
        BL4[Cache Service]
    end
    
    subgraph "Data Access Layer"
        DAL1[Database Manager]
        DAL2[Embeddings Service]
        DAL3[Rate Limiter]
    end
    
    subgraph "Infrastructure"
        INF1[(PostgreSQL)]
        INF2[(Redis)]
        INF3[OpenAI API]
    end
    
    UI1 --> BL1
    UI2 --> BL1
    
    BL1 --> BL2
    BL1 --> BL3
    BL2 --> BL4
    
    BL2 --> DAL1
    BL4 --> DAL2
    DAL1 --> INF1
    DAL2 --> INF1
    DAL2 --> INF3
    DAL3 --> INF2
    BL4 --> INF2
```

---

## 📦 Deployment Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx/Traefik]
    end
    
    subgraph "Application Instances"
        APP1[Backend Instance 1]
        APP2[Backend Instance 2]
        BOT1[Bot Instance 1]
    end
    
    subgraph "Data Tier"
        PG_M[(PostgreSQL Primary)]
        PG_R[(PostgreSQL Replica)]
        REDIS_M[(Redis Primary)]
        REDIS_R[(Redis Replica)]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
    end
    
    LB --> APP1
    LB --> APP2
    
    APP1 --> PG_M
    APP2 --> PG_M
    BOT1 --> PG_M
    
    APP1 --> REDIS_M
    APP2 --> REDIS_M
    BOT1 --> REDIS_M
    
    PG_M --> PG_R
    REDIS_M --> REDIS_R
    
    APP1 --> PROM
    APP2 --> PROM
    BOT1 --> PROM
    
    PROM --> GRAF
```

---

## 🔐 Security Architecture

```mermaid
graph TD
    USER[User Request] --> RLI[Rate Limiter<br/>10 req/min]
    RLI --> GUARD[Guardrails<br/>Security Checks]
    
    GUARD --> |Safe| PROC[Process Request]
    GUARD --> |Unsafe| BLOCK[Block & Log]
    
    PROC --> PII[PII Detection<br/>95% accuracy]
    PII --> |No PII| LLM[LLM Router]
    PII --> |PII Found| MASK[Mask & Warn]
    
    LLM --> RESP[Response]
    RESP --> VALIDATE[Response Validation]
    VALIDATE --> |OK| USER_RESP[Return to User]
    VALIDATE --> |Fail| ESC[Escalate]
    
    BLOCK --> AUDIT[Audit Log]
    MASK --> AUDIT
    ESC --> AUDIT
```

---

## 📊 Data Flow

```mermaid
flowchart LR
    subgraph "Input"
        Q[User Query]
    end
    
    subgraph "Preprocessing"
        LANG[Language Detection]
        GUARD[Security Check]
    end
    
    subgraph "Retrieval"
        CACHE{Cache?}
        DB[(Database)]
        VECTOR[pgvector Search]
    end
    
    subgraph "Generation"
        LLM[GPT-4]
        PROMPT[Prompt Engineering]
    end
    
    subgraph "Output"
        RESP[Response]
        LOG[Logging]
    end
    
    Q --> LANG
    LANG --> GUARD
    GUARD -->|Safe| CACHE
    
    CACHE -->|Hit| VECTOR
    CACHE -->|Miss| DB
    DB --> CACHE
    DB --> VECTOR
    
    VECTOR --> PROMPT
    PROMPT --> LLM
    LLM --> RESP
    
    RESP --> LOG
    RESP --> Q
```

---

## 🎯 Key Design Patterns

### **1. Dependency Injection**

```mermaid
classDiagram
    class Container {
        +config: Configuration
        +db_manager: DatabaseSessionManager
        +faq_service: FAQService
        +llm_router: LLMRouter
    }
    
    class FAQService {
        -session: AsyncSession
        +get_all_faq_items()
        +add_faq_item()
    }
    
    class LLMRouter {
        -faq_service: FAQService
        -guardrails: Guardrails
        +process_query()
    }
    
    Container --> FAQService : creates
    Container --> LLMRouter : creates
    LLMRouter --> FAQService : uses
```

---

### **2. Repository Pattern**

```mermaid
classDiagram
    class FAQRepository {
        <<interface>>
        +get_all()
        +get_by_id()
        +create()
        +update()
        +delete()
    }
    
    class PostgreSQLFAQRepository {
        -session: AsyncSession
        +get_all()
        +get_by_id()
    }
    
    class CachedFAQRepository {
        -repository: FAQRepository
        -cache: CacheService
        +get_all()
    }
    
    FAQRepository <|-- PostgreSQLFAQRepository : implements
    FAQRepository <|-- CachedFAQRepository : implements
    CachedFAQRepository --> FAQRepository : decorates
```

---

### **3. Cache-Aside Pattern**

```mermaid
sequenceDiagram
    participant Client
    participant Cache
    participant DB
    
    Client->>Cache: get(key)
    
    alt Cache Hit
        Cache-->>Client: value
    else Cache Miss
        Cache-->>Client: None
        Client->>DB: query()
        DB-->>Client: value
        Client->>Cache: set(key, value)
    end
```

---

## 📊 Technology Stack

```mermaid
graph TB
    subgraph "Frontend"
        TG[Telegram<br/>aiogram 3.x]
        WEB[React<br/>TypeScript]
    end
    
    subgraph "Backend"
        API[FastAPI<br/>Python 3.11]
        ASYNC[asyncio<br/>async/await]
    end
    
    subgraph "AI/ML"
        GPT[OpenAI GPT-4]
        EMB[text-embedding-3-small]
        VEC[pgvector<br/>ANN search]
    end
    
    subgraph "Storage"
        PG[PostgreSQL 15<br/>+pgvector]
        RD[Redis 7<br/>Cache + FSM]
    end
    
    subgraph "DevOps"
        DOCK[Docker]
        K8S[Kubernetes]
        GHA[GitHub Actions]
    end
    
    TG --> API
    WEB --> API
    API --> GPT
    API --> PG
    API --> RD
    GPT --> EMB
    PG --> VEC
```

---

## 🔄 State Machine (FSM)

```mermaid
stateDiagram-v2
    [*] --> START
    START --> LANGUAGE_SELECT: /start
    LANGUAGE_SELECT --> MAIN_MENU: Select RU/KK
    MAIN_MENU --> ASK_QUESTION: Ask question
    MAIN_MENU --> FAQ_BROWSE: Browse FAQ
    ASK_QUESTION --> MAIN_MENU: Answer received
    ASK_QUESTION --> ESCALATION: No answer found
    ESCALATION --> MAIN_MENU: Escalated
    FAQ_BROWSE --> MAIN_MENU: Back
    MAIN_MENU --> [*]: Exit
```

---

**Детальные диаграммы готовы! Architecture documented! ✅**


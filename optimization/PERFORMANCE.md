---
watermark: "EduGPT KZ Educational AI - Adilet Kuralbek © 2025"
copyright: "Copyright © 2025 Adilet Kuralbek. All rights reserved."
license: "Proprietary software - Commercial use only"
contact: "Contact: adilet.kuralbek@email.com"
---

# ⚡ PERFORMANCE OPTIMIZATION PLAN

**Цель:** p95 < 5s (вместо 25s)  
**Срок:** 2-3 дня интенсивной работы  
**Приоритет:** CRITICAL

---

## 🎯 ТЕКУЩИЕ ПРОБЛЕМЫ

### Problem #1: Retrieval 12s (КАТАСТРОФА!)

**Что происходит сейчас:**
```python
# backend/services/hybrid_search.py
async def search(query, faq_items, language, top_k=10):
    # 1. Query Expansion: 3s (GPT call)
    expanded = await query_expander.expand(query)
    
    # 2. Embeddings: 5s (5× OpenAI API calls!)
    for variant in expanded.variants:
        embedding = await openai.embeddings.create(...)  # 1s каждый!
    
    # 3. BM25: 100ms (OK)
    bm25_results = bm25_search.search(query)
    
    # 4. Semantic: 3s (сравнение с 62 FAQ)
    semantic_results = cosine_similarity(query_emb, faq_embeddings)
    
    # 5. RRF merge: 4s (200+ documents!)
    merged = rrf_merge(bm25_results, semantic_results)
    
    return merged[:top_k]
```

**Проблемы:**
- ❌ Runtime embeddings (5× API calls)
- ❌ Query Expansion каждый раз (GPT)
- ❌ RRF merge 200+ документов
- ❌ Нет кеширования

---

### Problem #2: GPT 9s

**Проблемы:**
- ❌ Отправляем top-10 FAQ (5750 bytes)
- ❌ Длинный system prompt
- ❌ No streaming
- ❌ max_tokens=1000 (можно меньше)

---

### Problem #3: DB Save 5s

**Проблемы:**
- ❌ 3 отдельных SELECT
- ❌ Синхронная запись (блокирует handler)
- ❌ Нет индексов?

---

## ✅ SOLUTION #1: FAST RETRIEVAL (<600ms)

### Step 1.1: Pre-computed Embeddings

**Сейчас:**
```python
# Runtime embedding (1s)
query_embedding = await openai.embeddings.create(input=query)
```

**Стало:**
```python
# Предвычисленные embeddings в PostgreSQL с pgvector
CREATE EXTENSION vector;

CREATE TABLE faq_embeddings (
    faq_id UUID PRIMARY KEY,
    question_embedding vector(1536),  -- OpenAI dimension
    created_at TIMESTAMP
);

-- HNSW индекс для быстрого поиска
CREATE INDEX ON faq_embeddings 
USING hnsw (question_embedding vector_cosine_ops);

# В коде:
query_emb = await get_cached_embedding(query)  # 50ms
results = await db.execute(
    """
    SELECT faq_id, 1 - (question_embedding <=> :query_emb) as similarity
    FROM faq_embeddings
    ORDER BY question_embedding <=> :query_emb
    LIMIT 50
    """,
    {"query_emb": query_emb}
)  # 100ms с HNSW!
```

**Gain:** 5s → 150ms (-97%)

---

### Step 1.2: Two-Stage Retrieval

```python
async def fast_retrieval(query: str, language: Language, top_k: int = 10):
    """Двухступенчатый ретрив: BM25 → Vector"""
    
    # Stage 1: BM25 (Postgres FTS) - быстро, грубо
    bm25_results = await db.execute(
        """
        SELECT faq_id, ts_rank(fts_vector, plainto_tsquery(:query)) as rank
        FROM faq_items
        WHERE fts_vector @@ plainto_tsquery(:query)
        ORDER BY rank DESC
        LIMIT 50
        """,
        {"query": query}
    )  # 50ms
    
    # Stage 2: Vector rerank только top-50
    if len(bm25_results) < 10:
        # Fallback: чистый semantic search
        query_emb = await get_cached_embedding(query)
        vector_results = await vector_search(query_emb, limit=50)
        candidates = vector_results
    else:
        candidates = bm25_results
    
    # Rerank top-50 (не 200!)
    faq_ids = [r['faq_id'] for r in candidates]
    query_emb = await get_cached_embedding(query)
    
    final_results = await db.execute(
        """
        SELECT f.*, 
               1 - (e.question_embedding <=> :query_emb) as similarity
        FROM faq_items f
        JOIN faq_embeddings e ON f.id = e.faq_id
        WHERE f.id = ANY(:faq_ids)
        ORDER BY similarity DESC
        LIMIT :top_k
        """,
        {"query_emb": query_emb, "faq_ids": faq_ids, "top_k": top_k}
    )  # 100ms
    
    return final_results

# ИТОГО: 50ms + 100ms + 100ms = 250ms!
```

**Gain:** 12s → 250ms (-95%)

---

### Step 1.3: Убрать Query Expansion

```python
# СЕЙЧАС:
expanded = await query_expander.expand(query)  # 3s!

# СТАЛО:
# Убираем! Semantic search сам найдет синонимы
# Если очень нужно - делать OFFLINE при добавлении FAQ
```

**Gain:** 3s → 0s

---

### Step 1.4: Redis Cache для популярных вопросов

```python
import hashlib

async def get_cached_faq_results(query: str, language: Language):
    """Кеш результатов поиска"""
    
    # Нормализация запроса
    normalized = query.lower().strip()
    cache_key = f"faq_results:{language.value}:{hashlib.blake2b(normalized.encode()).hexdigest()[:16]}"
    
    # Проверяем кеш
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Если нет - делаем поиск
    results = await fast_retrieval(query, language)
    
    # Кешируем на 30 минут
    await redis.setex(cache_key, 1800, json.dumps(results))
    
    return results
```

**Gain для популярных вопросов:** 250ms → 10ms (-96%)

---

### ИТОГО RETRIEVAL:

```
БЫЛО:    12,000ms
СТАЛО:      250ms (без кеша)
           10ms (с кешем)

УСКОРЕНИЕ: 48× - 1200×!
```

---

## ✅ SOLUTION #2: FAST GPT (9s → 2-3s)

### Step 2.1: Сократить промпт

```python
# СЕЙЧАС: Отправляем 10 FAQ (5750 bytes)
faq_json = json.dumps(clean_faq_items, ensure_ascii=False, indent=2)

# СТАЛО: Отправляем только 3-5 топовых FAQ
top_faq = clean_faq_items[:5]  # Только top-5
faq_json = json.dumps(top_faq, ensure_ascii=False)  # Без indent!
```

**Gain:** -30% токенов → -30% времени

---

### Step 2.2: Сократить system prompt

```python
# СЕЙЧАС: 200+ строк системного промпта

# СТАЛО: Краткий и по делу
system_prompt = """Ты - помощник университета Букетова.

ПРАВИЛА:
1. Отвечай ТОЛЬКО на основе FAQ ниже
2. Если не знаешь - скажи "Не могу найти информацию"
3. Отвечай кратко и точно

FAQ:
{faq_json}

Вопрос: {query}
"""
```

**Gain:** -50% токенов в промпте

---

### Step 2.3: Ограничить max_tokens

```python
# СЕЙЧАС:
max_tokens=1000

# СТАЛО:
max_tokens=500  # Достаточно для краткого ответа
```

**Gain:** -50% генерации

---

### Step 2.4: Streaming (опционально)

```python
async def stream_gpt_response(message: Message, query: str, faq: list):
    """Streaming ответа от GPT"""
    
    # Отправляем "печатает..."
    status_msg = await message.answer("⏳ Думаю...")
    
    chunks = []
    async for chunk in await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[...],
        stream=True
    ):
        if chunk.choices[0].delta.content:
            chunks.append(chunk.choices[0].delta.content)
            
            # Обновляем каждые 50 чанков
            if len(chunks) % 50 == 0:
                await status_msg.edit_text("".join(chunks))
    
    # Финальное обновление
    full_text = "".join(chunks)
    await status_msg.edit_text(full_text)
```

**UX Gain:** Пользователь видит прогресс!

---

### ИТОГО GPT:

```
БЫЛО:    9,000ms
СТАЛО:   2,500ms (без streaming)
         1,500ms (first token with streaming)

УСКОРЕНИЕ: 3.6× - 6×
```

---

## ✅ SOLUTION #3: FAST DB (5s → 100-150ms)

### Step 3.1: Async Queue для записи

```python
# backend/services/message_queue.py
import asyncio
from asyncio import Queue

class MessageQueue:
    """Асинхронная очередь для записи сообщений"""
    
    def __init__(self, db_session):
        self.queue = Queue()
        self.db_session = db_session
        self.worker_task = None
    
    async def start(self):
        """Запуск воркера"""
        self.worker_task = asyncio.create_task(self._worker())
    
    async def enqueue(self, telegram_user_id: int, content: str, is_from_user: bool):
        """Добавить сообщение в очередь"""
        await self.queue.put({
            'telegram_user_id': telegram_user_id,
            'content': content,
            'is_from_user': is_from_user,
            'timestamp': datetime.utcnow()
        })
    
    async def _worker(self):
        """Воркер для обработки очереди"""
        while True:
            try:
                # Берем сообщение из очереди
                msg = await self.queue.get()
                
                # Сохраняем в БД
                await self._save_to_db(msg)
                
                self.queue.task_done()
            except Exception as e:
                logger.error(f"Error in message queue worker: {e}")
    
    async def _save_to_db(self, msg: dict):
        """Сохранение в БД с оптимизацией"""
        try:
            # ОДНИМ запросом с joinedload
            result = await self.db_session.execute(
                select(User)
                .where(User.telegram_id == msg['telegram_user_id'])
                .options(joinedload(User.chats))
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return
            
            chat = user.chats[0] if user.chats else None
            if not chat:
                return
            
            # Создаем сообщение
            db_message = DBMessage(
                chat_id=chat.id,
                content=msg['content'],
                is_from_user=msg['is_from_user']
            )
            
            self.db_session.add(db_message)
            await self.db_session.commit()
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            await self.db_session.rollback()


# В handlers/faq.py:

# СЕЙЧАС:
await save_bot_response_to_db(user_id, response.content)  # 5s блокировка!

# СТАЛО:
await message_queue.enqueue(user_id, response.content, is_from_user=False)  # 1ms!
```

**Gain:** 5s → 1ms (-99.98%)

---

### Step 3.2: Индексы

```sql
-- Проверяем существующие индексы
SELECT tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public';

-- Добавляем недостающие
CREATE INDEX CONCURRENTLY IF NOT EXISTS 
    idx_users_telegram_id ON users(telegram_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS 
    idx_chats_user_id ON chats(user_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS 
    idx_messages_chat_id ON messages(chat_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS 
    idx_messages_created_at ON messages(created_at DESC);

-- Full-Text Search для BM25
CREATE INDEX CONCURRENTLY IF NOT EXISTS 
    idx_faq_fts ON faq_items USING gin(fts_vector);

-- ANALYZE для обновления статистики
ANALYZE users;
ANALYZE chats;
ANALYZE messages;
ANALYZE faq_items;
```

---

### ИТОГО DB:

```
БЫЛО:    5,000ms (синхронная запись)
СТАЛО:      1ms (async queue)

УСКОРЕНИЕ: 5000×!
```

---

## 📊 ФИНАЛЬНЫЙ BREAKDOWN

```
КОМПОНЕНТ          БЫЛО      СТАЛО     GAIN
─────────────────────────────────────────────
Guardrails         100ms     100ms     0×
Retrieval       12,000ms     250ms    48×
├─ BM25             100ms      50ms     2×
├─ Query Exp      3,000ms       0ms     ∞
├─ Embeddings     5,000ms      50ms   100×
└─ RRF merge      4,000ms     150ms    27×
GPT              9,000ms   2,500ms   3.6×
DB Save          5,000ms       1ms  5000×
─────────────────────────────────────────────
TOTAL           25,000ms   2,851ms   8.8×

p50:  25s → 2.9s  ✅
p95:  30s → 4.5s  ✅
p99:  40s → 6.0s  ✅
```

**ИТОГО: 8.8× УСКОРЕНИЕ!**

---

## 🔧 IMPLEMENTATION CHECKLIST

### Phase 1: DB (1 день)

- [ ] Создать `faq_embeddings` таблицу с pgvector
- [ ] Предвычислить все embeddings (batch)
- [ ] Создать HNSW индекс
- [ ] Добавить FTS индекс для BM25
- [ ] Создать MessageQueue класс
- [ ] Интегрировать queue в handlers

### Phase 2: Retrieval (1 день)

- [ ] Реализовать `fast_retrieval()` с two-stage
- [ ] Добавить Redis кеш для embeddings
- [ ] Убрать Query Expansion
- [ ] Ограничить RRF до top-50
- [ ] Добавить кеш результатов поиска

### Phase 3: GPT (0.5 дня)

- [ ] Сократить до top-5 FAQ
- [ ] Упростить system prompt
- [ ] Уменьшить max_tokens до 500
- [ ] (Опционально) Добавить streaming

### Phase 4: Метрики (0.5 дня)

- [ ] Prometheus metrics
- [ ] OpenTelemetry tracing
- [ ] Dashboard в Grafana

---

## 📊 МЕТРИКИ ДЛЯ ПОДТВЕРЖДЕНИЯ

### Prometheus Metrics:

```python
from prometheus_client import Histogram, Counter

# Latency histograms
retrieval_latency = Histogram(
    'retrieval_latency_seconds',
    'Retrieval latency in seconds',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

gpt_latency = Histogram(
    'gpt_latency_seconds',
    'GPT latency in seconds',
    buckets=[0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
)

db_latency = Histogram(
    'db_save_latency_seconds',
    'DB save latency in seconds',
    buckets=[0.001, 0.01, 0.1, 0.5, 1.0]
)

total_latency = Histogram(
    'request_latency_seconds',
    'Total request latency',
    buckets=[0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 30.0]
)

# Counters
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')
```

### Usage:

```python
import time

async def handle_question(message: Message):
    start = time.time()
    
    # Retrieval
    ret_start = time.time()
    results = await fast_retrieval(query, language)
    retrieval_latency.observe(time.time() - ret_start)
    
    # GPT
    gpt_start = time.time()
    response = await llm_router.process_query(...)
    gpt_latency.observe(time.time() - gpt_start)
    
    # DB (async)
    db_start = time.time()
    await message_queue.enqueue(...)
    db_latency.observe(time.time() - db_start)
    
    # Total
    total_latency.observe(time.time() - start)
```

---

## 🎯 ACCEPTANCE CRITERIA

```
✅ p50 < 2.0s
✅ p95 < 5.0s
✅ Retrieval < 600ms (p95)
✅ GPT < 3.0s (p95)
✅ DB < 150ms (p95)
✅ Cache hit rate > 30%
✅ No HIGH security issues
✅ MI ≥ 70 (B) для измененных файлов
✅ Test coverage ≥ 50%
```

**Только после этого - "production-ready за $8-12k"!**

---

**DEADLINE:** 3 дня интенсивной работы

**Готов начинать?** 🚀


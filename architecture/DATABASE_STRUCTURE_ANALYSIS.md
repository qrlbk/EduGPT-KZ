---
watermark: "EduGPT KZ Educational AI - Adilet Kuralbek © 2025"
copyright: "Copyright © 2025 Adilet Kuralbek. All rights reserved."
license: "Proprietary software - Commercial use only"
contact: "Contact: adilet.kuralbek@email.com"
---

# 🔍 АНАЛИЗ СТРУКТУРЫ БАЗЫ ДАННЫХ

## ПРОБЛЕМА

В базе данных **две версии FAQ таблиц**:

### 1. Старая структура (НЕ используется):
```sql
faq                  -- Старая таблица FAQ
├── question         -- Вопрос в самой таблице ❌
├── answer           -- Ответ в самой таблице ❌
└── ...
```

### 2. Новая структура (ИСПОЛЬЗУЕТСЯ):
```sql
faq_items            -- Основная таблица
├── id
├── title            -- Заголовок вопроса
├── title_kk
├── category
├── priority
└── ...

faq_questions        -- Таблица вопросов ✅
├── faq_item_id      -- Связь с faq_items
├── question_text    -- Текст вопроса
└── language         -- ru / kk

faq_answers          -- Таблица ответов ✅
├── faq_item_id      -- Связь с faq_items
├── answer_text      -- Текст ответа
└── language         -- ru / kk
```

## ТАКЖЕ В faq_items ЕСТЬ СТАРЫЕ КОЛОНКИ:

```sql
faq_items
├── question         ❌ УДАЛИТЬ (не используется)
├── answer           ❌ УДАЛИТЬ (не используется)  
├── keywords         ❌ УДАЛИТЬ (JSON, не нужен)
├── last_validated   ❌ УДАЛИТЬ (не используется)
```

## РЕШЕНИЕ

### Вариант 1: Очистить через миграцию
Создать новую миграцию Alembic которая:
1. Удалит таблицу `faq`
2. Удалит колонки `question`, `answer`, `keywords`, `last_validated` из `faq_items`

### Вариант 2: Очистить вручную через SQL
```sql
-- Удалить старые колонки
ALTER TABLE faq_items DROP COLUMN IF EXISTS question;
ALTER TABLE faq_items DROP COLUMN IF EXISTS answer;
ALTER TABLE faq_items DROP COLUMN IF EXISTS keywords;
ALTER TABLE faq_items DROP COLUMN IF EXISTS last_validated;

-- Удалить старую таблицу
DROP TABLE IF EXISTS faq CASCADE;
```

## РЕКОМЕНДАЦИЯ

Выполнить Вариант 2 (быстрее) и перезапустить бот.


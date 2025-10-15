-- EduGPT KZ - Database Schema Demo
-- Автор: Adilet Kuralbek
-- © 2025. All rights reserved.

-- ===========================================
-- ДЕМОНСТРАЦИОННАЯ СХЕМА БАЗЫ ДАННЫХ
-- ===========================================
-- ВАЖНО: Это упрощенная схема для демонстрации.
-- Полная схема с индексами, триггерами и оптимизациями
-- доступна в коммерческой версии.

-- Создание базы данных
CREATE DATABASE edugpt_kz_demo;

-- Подключение к базе
\c edugpt_kz_demo;

-- Включение расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- ===========================================
-- ОСНОВНЫЕ ТАБЛИЦЫ
-- ===========================================

-- Пользователи системы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    language VARCHAR(10) DEFAULT 'ru',
    role VARCHAR(20) DEFAULT 'student', -- student, teacher, admin
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FAQ элементы
CREATE TABLE faq_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high
    confidence_threshold DECIMAL(3,2) DEFAULT 0.8,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FAQ вопросы (нормализованная структура)
CREATE TABLE faq_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    faq_item_id UUID REFERENCES faq_items(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FAQ ответы (нормализованная структура)
CREATE TABLE faq_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    faq_item_id UUID REFERENCES faq_items(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Сообщения пользователей
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    telegram_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    is_from_user BOOLEAN NOT NULL,
    language VARCHAR(10),
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Аналитика и метрики
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL, -- message_sent, faq_search, user_registration
    user_id INTEGER REFERENCES users(id),
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- ВЕКТОРНЫЙ ПОИСК (PGVECTOR)
-- ===========================================

-- Векторные представления FAQ для семантического поиска
CREATE TABLE faq_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    faq_item_id UUID REFERENCES faq_items(id) ON DELETE CASCADE,
    embedding VECTOR(1536), -- OpenAI embeddings dimension
    text_content TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    model_version VARCHAR(50) DEFAULT 'text-embedding-3-small',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- ИНДЕКСЫ ДЛЯ ПРОИЗВОДИТЕЛЬНОСТИ
-- ===========================================

-- Индексы для быстрого поиска
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_language ON users(language);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_faq_items_category ON faq_items(category);
CREATE INDEX idx_faq_items_priority ON faq_items(priority);

-- Векторный индекс для семантического поиска
CREATE INDEX idx_faq_embeddings_vector ON faq_embeddings 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- JSONB индекс для аналитики
CREATE INDEX idx_analytics_data ON analytics_events USING GIN (data);

-- ===========================================
-- ТРИГГЕРЫ И ФУНКЦИИ
-- ===========================================

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггеры для автоматического обновления updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_faq_items_updated_at BEFORE UPDATE ON faq_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- ДЕМО ДАННЫЕ
-- ===========================================

-- Вставка демо пользователей
INSERT INTO users (telegram_id, username, first_name, language, role) VALUES
(12345, 'student_demo', 'Айдар', 'kk', 'student'),
(54321, 'teacher_demo', 'Гульнара', 'ru', 'teacher'),
(99999, 'admin_demo', 'Админ', 'ru', 'admin');

-- Вставка демо FAQ элементов
INSERT INTO faq_items (title, category, priority) VALUES
('Расписание занятий', 'Расписание', 'high'),
('Экзамены', 'Экзамены', 'high'),
('Стипендия', 'Финансы', 'medium'),
('Контактная информация', 'Общие', 'medium');

-- Получение ID для связывания
DO $$
DECLARE
    schedule_id UUID;
    exam_id UUID;
    stipend_id UUID;
    contact_id UUID;
BEGIN
    SELECT id INTO schedule_id FROM faq_items WHERE title = 'Расписание занятий';
    SELECT id INTO exam_id FROM faq_items WHERE title = 'Экзамены';
    SELECT id INTO stipend_id FROM faq_items WHERE title = 'Стипендия';
    SELECT id INTO contact_id FROM faq_items WHERE title = 'Контактная информация';

    -- FAQ вопросы на русском
    INSERT INTO faq_questions (faq_item_id, question_text, language) VALUES
    (schedule_id, 'Где мое расписание?', 'ru'),
    (schedule_id, 'Когда у меня занятия?', 'ru'),
    (exam_id, 'Когда экзамен по математике?', 'ru'),
    (exam_id, 'Расписание экзаменов', 'ru'),
    (stipend_id, 'Сколько стипендия?', 'ru'),
    (stipend_id, 'Когда выплачивается стипендия?', 'ru'),
    (contact_id, 'Контакты приемной комиссии', 'ru'),
    (contact_id, 'Телефон университета', 'ru');

    -- FAQ ответы на русском
    INSERT INTO faq_answers (faq_item_id, answer_text, language) VALUES
    (schedule_id, 'Расписание доступно в личном кабинете e.edugpt.edu.kz в разделе "Расписание"', 'ru'),
    (exam_id, 'Расписание экзаменов публикуется за 2 недели до начала сессии', 'ru'),
    (stipend_id, 'Стипендия составляет 50,000 тенге и выплачивается 10 числа каждого месяца', 'ru'),
    (contact_id, 'Приемная комиссия: +7 (727) 377-33-33, email: info@edugpt.edu.kz', 'ru');

    -- FAQ вопросы на казахском
    INSERT INTO faq_questions (faq_item_id, question_text, language) VALUES
    (schedule_id, 'Сабақ кестем қайда?', 'kk'),
    (exam_id, 'Емтихан қашан?', 'kk'),
    (stipend_id, 'Стипендия қанша?', 'kk'),
    (contact_id, 'Байланыс мәліметтері', 'kk');

    -- FAQ ответы на казахском
    INSERT INTO faq_answers (faq_item_id, answer_text, language) VALUES
    (schedule_id, 'Сабақ кестесі e.edugpt.edu.kz сайтындағы жеке кабинетте', 'kk'),
    (exam_id, 'Емтихан кестесі сессия басталмас бұрын 2 апта бұрын жарияланады', 'kk'),
    (stipend_id, 'Стипендия 50,000 теңге, әр айдың 10-ында төленеді', 'kk'),
    (contact_id, 'Қабылдау комиссиясы: +7 (727) 377-33-33, email: info@edugpt.edu.kz', 'kk');
END $$;

-- ===========================================
-- ПРЕДСТАВЛЕНИЯ ДЛЯ УДОБСТВА
-- ===========================================

-- Полное представление FAQ с вопросами и ответами
CREATE VIEW faq_full_view AS
SELECT 
    fi.id,
    fi.title,
    fi.category,
    fi.priority,
    fi.confidence_threshold,
    fq.question_text,
    fq.language as question_language,
    fa.answer_text,
    fa.language as answer_language,
    fi.created_at,
    fi.updated_at
FROM faq_items fi
LEFT JOIN faq_questions fq ON fi.id = fq.faq_item_id
LEFT JOIN faq_answers fa ON fi.id = fa.faq_item_id;

-- Статистика пользователей
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.telegram_id,
    u.username,
    u.first_name,
    u.language,
    u.role,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message_at
FROM users u
LEFT JOIN messages m ON u.id = m.user_id
GROUP BY u.id, u.telegram_id, u.username, u.first_name, u.language, u.role;

-- ===========================================
-- ФУНКЦИИ ДЛЯ ПОИСКА
-- ===========================================

-- Функция поиска FAQ по тексту
CREATE OR REPLACE FUNCTION search_faq(
    search_query TEXT,
    search_language VARCHAR(10) DEFAULT 'ru',
    limit_count INTEGER DEFAULT 5
)
RETURNS TABLE (
    faq_id UUID,
    title VARCHAR(500),
    answer_text TEXT,
    relevance_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        fi.id,
        fi.title,
        fa.answer_text,
        ts_rank(to_tsvector(search_language, fa.answer_text), 
                plainto_tsquery(search_language, search_query)) as relevance
    FROM faq_items fi
    JOIN faq_answers fa ON fi.id = fa.faq_item_id
    WHERE fa.language = search_language
    AND to_tsvector(search_language, fa.answer_text) @@ plainto_tsquery(search_language, search_query)
    ORDER BY relevance DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- ===========================================
-- КОММЕНТАРИИ И ДОКУМЕНТАЦИЯ
-- ===========================================

COMMENT ON DATABASE edugpt_kz_demo IS 'Демонстрационная база данных EduGPT KZ - AI Assistant for Universities';
COMMENT ON TABLE users IS 'Пользователи системы (студенты, преподаватели, администраторы)';
COMMENT ON TABLE faq_items IS 'Основные элементы FAQ с метаданными';
COMMENT ON TABLE faq_questions IS 'Вопросы FAQ (нормализованная структура)';
COMMENT ON TABLE faq_answers IS 'Ответы FAQ (нормализованная структура)';
COMMENT ON TABLE messages IS 'Сообщения пользователей и ответы бота';
COMMENT ON TABLE analytics_events IS 'События для аналитики и метрик';
COMMENT ON TABLE faq_embeddings IS 'Векторные представления FAQ для семантического поиска';

-- ===========================================
-- ПРИМЕЧАНИЯ
-- ===========================================

/*
ВАЖНО: Это демонстрационная схема базы данных.

Полная версия включает:
- Дополнительные таблицы для модерации
- Расширенную аналитику
- Систему уведомлений
- Интеграции с внешними сервисами
- Продвинутые индексы и оптимизации
- Систему резервного копирования
- Мониторинг производительности

Для получения полной схемы обращайтесь:
📧 kuralbekadilet475@gmail.com
*/

-- Завершение
\echo '✅ Демонстрационная схема базы данных создана успешно!'
\echo '📊 Таблиц создано: 7'
\echo '📈 Индексов создано: 8'
\echo '🔧 Функций создано: 3'
\echo '📋 Представлений создано: 2'
\echo ''
\echo '⚖️ © 2025 Adilet Kuralbek. All rights reserved.'

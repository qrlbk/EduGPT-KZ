# 📡 API Documentation - EduGPT KZ

## 🎯 Обзор API

EduGPT KZ предоставляет RESTful API для интеграции с внешними системами и управления ботом.

## 🔗 Base URL

```
Production: https://api.edugpt.kz
Development: http://localhost:8000
```

## 🔐 Аутентификация

### JWT Token
```http
Authorization: Bearer <your_jwt_token>
```

### Получение токена
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

## 📋 Основные endpoints

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "ai_service": "available"
  }
}
```

### 2. Отправка сообщения
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Когда экзамен по математике?",
  "user_id": 12345,
  "language": "ru",
  "context": {
    "session_id": "abc123",
    "previous_messages": []
  }
}
```

**Response:**
```json
{
  "response": "Экзамен по математике назначен на 15 декабря в 9:00 в аудитории 201.",
  "confidence": 0.95,
  "sources": [
    {
      "type": "faq",
      "id": "faq_123",
      "relevance": 0.98
    }
  ],
  "response_time_ms": 1200,
  "session_id": "abc123"
}
```

### 3. Поиск в FAQ
```http
GET /api/faq/search?query=расписание&language=ru&limit=5
```

**Response:**
```json
{
  "results": [
    {
      "id": "faq_456",
      "question": "Где найти расписание занятий?",
      "answer": "Расписание доступно в личном кабинете...",
      "category": "Расписание",
      "relevance_score": 0.95
    }
  ],
  "total": 1,
  "query": "расписание",
  "language": "ru"
}
```

### 4. Управление FAQ
```http
POST /api/admin/faq
Content-Type: application/json

{
  "title": "Новый FAQ",
  "questions": [
    {
      "text": "Как получить справку?",
      "language": "ru"
    }
  ],
  "answers": [
    {
      "text": "Справку можно получить в деканате...",
      "language": "ru"
    }
  ],
  "category": "Документы",
  "priority": "medium"
}
```

### 5. Аналитика
```http
GET /api/analytics/stats?period=7d
```

**Response:**
```json
{
  "period": "7d",
  "metrics": {
    "total_users": 1250,
    "active_users": 890,
    "total_messages": 15420,
    "avg_response_time_ms": 1200,
    "faq_hit_rate": 0.85,
    "user_satisfaction": 4.7
  },
  "trends": {
    "users_growth": 0.12,
    "messages_growth": 0.08
  }
}
```

## 📊 Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос |
| 201 | Ресурс создан |
| 400 | Неверный запрос |
| 401 | Не авторизован |
| 403 | Доступ запрещен |
| 404 | Ресурс не найден |
| 429 | Превышен лимит запросов |
| 500 | Внутренняя ошибка сервера |

## 🚦 Rate Limiting

### Лимиты по типам пользователей
- **Студенты:** 100 запросов/час
- **Преподаватели:** 500 запросов/час  
- **Администраторы:** 1000 запросов/час

### Headers для rate limiting
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

## 🔍 Фильтрация и пагинация

### Пагинация
```http
GET /api/messages?page=1&limit=20&offset=0
```

### Сортировка
```http
GET /api/messages?sort=created_at&order=desc
```

### Фильтрация
```http
GET /api/messages?user_id=12345&date_from=2025-01-01&date_to=2025-01-31
```

## 📝 Webhook уведомления

### Конфигурация webhook
```http
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["message_received", "faq_updated"],
  "secret": "your_webhook_secret"
}
```

### Формат webhook payload
```json
{
  "event": "message_received",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "user_id": 12345,
    "message": "Когда экзамен?",
    "response": "15 декабря в 9:00"
  },
  "signature": "sha256=..."
}
```

## 🧪 Тестирование API

### Postman Collection
Импортируйте коллекцию Postman для тестирования всех endpoints:
```
docs/api/postman_collection.json
```

### cURL примеры
```bash
# Health check
curl -X GET http://localhost:8000/api/health

# Отправка сообщения
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Когда экзамен?", "user_id": 12345}'

# Поиск в FAQ
curl -X GET "http://localhost:8000/api/faq/search?query=расписание&language=ru"
```

## 📚 SDK и библиотеки

### Python SDK
```python
from edugpt_client import EduGPTClient

client = EduGPTClient(api_key="your_api_key")
response = client.send_message("Когда экзамен?", user_id=12345)
print(response.text)
```

### JavaScript SDK
```javascript
import { EduGPTClient } from 'edugpt-client';

const client = new EduGPTClient({ apiKey: 'your_api_key' });
const response = await client.sendMessage('Когда экзамен?', 12345);
console.log(response.text);
```

## 🔧 Настройка и конфигурация

### Переменные окружения
```bash
API_HOST=localhost
API_PORT=8000
JWT_SECRET=your_secret_key
RATE_LIMIT_ENABLED=true
CORS_ORIGINS=http://localhost:3000,https://admin.edugpt.kz
```

### Конфигурация логирования
```yaml
logging:
  level: INFO
  format: json
  handlers:
    - console
    - file
  file_path: /var/log/edugpt-api.log
```

## 🛡️ Безопасность

### HTTPS
Все production endpoints используют HTTPS с TLS 1.3.

### Валидация входных данных
- JSON Schema валидация
- Sanitization пользовательского ввода
- Rate limiting и DDoS защита

### Audit Logging
Все API вызовы логируются для аудита:
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "method": "POST",
  "endpoint": "/api/chat/message",
  "user_id": 12345,
  "ip_address": "192.168.1.100",
  "response_time_ms": 1200,
  "status_code": 200
}
```

---

*Полная документация API доступна в коммерческой версии с дополнительными endpoints и функциями.*

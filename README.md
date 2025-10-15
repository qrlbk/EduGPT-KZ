# EduGPT KZ — AI Assistant for Universities 🇰🇿

<div align="center">

![EduGPT Logo](https://img.shields.io/badge/EduGPT-KZ-blue?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue?style=for-the-badge&logo=postgresql&logoColor=white)

**Автор:** Adilet Kuralbek  
**© 2025. All rights reserved.**  
**Контакты:** kuralbekadilet475@gmail.com

---

### 🇺🇸 English Description

**EduGPT KZ** is an intelligent AI assistant specifically designed for universities in Kazakhstan. The system supports Kazakh and Russian languages, providing students and faculty with quick access to academic information.

**Key Features:**
- Multilingual AI assistant (Kazakh/Russian)
- Intelligent FAQ system with semantic search
- Specialized modules for students and teachers
- Analytics and monitoring capabilities
- Security and content moderation
- Telegram interface for easy access

**Tech Stack:** FastAPI, PostgreSQL, OpenAI GPT-4, pgvector, Redis, aiogram

> ⚠️ **IMPORTANT:** This repository contains a **demonstration version** of the system. The full commercial version (Enterprise Edition) is available upon request and includes advanced features, admin panel, full integration, and technical support.

---

</div>

---

## 🎯 О проекте

EduGPT KZ — это интеллектуальный AI-ассистент, специально разработанный для университетов Казахстана. Система поддерживает казахский и русский языки, обеспечивая студентов и преподавателей быстрым доступом к академической информации.

> ⚠️ **ВАЖНО:** Этот репозиторий содержит **демонстрационную часть** системы. Полная коммерческая версия (Enterprise Edition) предоставляется по запросу и включает расширенные возможности, админ-панель, полную интеграцию и техническую поддержку.

### ✨ Ключевые возможности

- 🤖 **Многоязычный AI-ассистент** (казахский, русский)
- 📚 **Интеллектуальный поиск** по базе знаний университета
- 🎓 **Специализированные модули** для студентов и преподавателей
- 📊 **Аналитика и мониторинг** взаимодействий
- 🔒 **Безопасность и модерация** контента
- 📱 **Telegram-интерфейс** для удобного доступа

---

## 🏗️ Архитектура

### Технологический стек

```
Frontend: Telegram Bot (aiogram 3.x)
Backend: FastAPI + PostgreSQL + Redis
AI: OpenAI GPT-4 + pgvector embeddings
Monitoring: Grafana + Prometheus
Deployment: Docker + Nginx
```

### Основные компоненты

- **API Gateway**: FastAPI с аутентификацией и rate limiting
- **Vector Database**: PostgreSQL с pgvector для семантического поиска
- **Caching Layer**: Redis для оптимизации производительности
- **Admin Panel**: Веб-интерфейс для управления и мониторинга
- **Analytics Engine**: Система сбора и анализа метрик

---

## 📁 Структура проекта

```
EduGPT-KZ/
├── 📖 README.md              # Этот файл
├── ⚖️ LICENSE.txt            # Лицензия (All Rights Reserved)
├── 📁 demo/                  # Демонстрационные материалы
│   ├── screenshots/          # Скриншоты интерфейса
│   ├── examples/             # Примеры диалогов
│   └── videos/               # Демо-видео
├── 📁 docs/                  # Техническая документация
│   ├── architecture/         # Архитектурные диаграммы
│   ├── api/                  # API документация
│   └── deployment/           # Гайды по развертыванию
└── 📁 open_source/           # Демо-код и примеры
    ├── basic_bot/            # Базовая реализация бота
    ├── api_examples/         # Примеры использования API
    └── database_schema/      # Схема базы данных
```

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- PostgreSQL 15+ с pgvector
- Redis 7+
- Docker & Docker Compose

### Установка демо-версии

```bash
# Клонирование репозитория
git clone https://github.com/kuralbekadilet475/EduGPT-KZ.git
cd EduGPT-KZ

# Переход в демо-директорию
cd open_source/basic_bot

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл с вашими настройками

# Запуск демо-бота
python demo_bot.py
```

---

## 📊 Демонстрация

### 🎥 Демо-видео
> **Скоро:** Видео-демонстрация работы системы будет добавлена в раздел [demo/videos/](demo/videos/)

### 📱 Скриншоты интерфейса
> **Добавьте скриншоты:** Разместите изображения интерфейса в папке [demo/screenshots/](demo/screenshots/) для визуального представления системы

### 💬 Примеры диалогов

**Студент:** "Когда экзамен по математике?"  
**EduGPT:** "Экзамен по математическому анализу назначен на 15 декабря в 9:00 в аудитории 201. Не забудьте взять с собой калькулятор и студенческий билет."

**Преподаватель:** "Как добавить новый FAQ?"  
**EduGPT:** "Для добавления нового FAQ используйте админ-панель: 1) Войдите в систему 2) Перейдите в раздел 'FAQ Management' 3) Нажмите 'Add New' 4) Заполните поля и сохраните."

**Многоязычность:**  
**Студент (казахский):** "Сабақ кестем қайда?"  
**EduGPT:** "Сабақ кестесі e.edugpt.edu.kz сайтындағы жеке кабинетте 'Сабақ кестесі' бөлімінде"

---

## 🔧 API Документация

### Основные endpoints

```http
GET /api/health
POST /api/chat/message
GET /api/faq/search?query=...
GET /api/analytics/stats
```

### Пример запроса

```bash
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Как узнать расписание?",
    "user_id": "12345",
    "language": "ru"
  }'
```

---

## 📈 Производительность

- ⚡ **Время отклика**: < 2 секунд
- 🔄 **Пропускная способность**: 1000+ запросов/минуту
- 🎯 **Точность ответов**: 95%+ для FAQ
- 📊 **Uptime**: 99.9%

---

## 🛡️ Безопасность

- 🔐 JWT аутентификация
- 🚦 Rate limiting и DDoS защита
- 🔍 Контент-модерация
- 📝 Логирование всех действий
- 🛡️ Валидация входных данных

---

## 💼 Коммерческое использование

> ⚠️ **ВАЖНО:** Любое коммерческое использование, включая развертывание, интеграцию или получение прибыли от данного кода, **СТРОГО ЗАПРЕЩЕНО** без письменного разрешения автора.

### Для коммерческого использования доступны:

- 🏢 **Enterprise Edition** — полная версия с расширенными возможностями и технической поддержкой
- 🎓 **University License** — специальная лицензия для образовательных учреждений
- 🤝 **White-label Solution** — брендированное решение под вашу организацию
- 🔧 **Custom Development** — индивидуальная разработка под ваши требования
- 🛡️ **Full Source Code** — полный исходный код с документацией

### Контакты для бизнес-вопросов:

📧 **Email:** kuralbekadilet475@gmail.com  
💼 **LinkedIn:** [Adilet Kuralbek](https://linkedin.com/in/adilet-kuralbek)  
📱 **Telegram:** @kuralbekadilet

---


## 📚 Документация

- 📖 [Архитектура системы](docs/architecture/README.md)
- 🔌 [API Reference](docs/api/README.md)
- 🚀 [Deployment Guide](docs/deployment/README.md)
- 🧪 [Testing Guide](docs/testing/README.md)

---

## 🤝 Вклад в проект

Этот проект является **проприетарным**. Если вы заинтересованы в сотрудничестве:

1. 📧 Свяжитесь с автором
2. 💼 Обсудите возможности партнерства
3. 🤝 Рассмотрите коммерческое лицензирование

---

## ⚖️ Лицензия

```
© 2025 Adilet Kuralbek. All rights reserved.

Этот проект защищен авторским правом.
Использование без разрешения запрещено.
```

**Полные условия лицензии:** [LICENSE.txt](LICENSE.txt)

---

<div align="center">

**Сделано с ❤️ в Казахстане**

![Kazakhstan Flag](https://img.shields.io/badge/Made%20in-Kazakhstan-yellow?style=for-the-badge&logo=flag&logoColor=white)

*EduGPT KZ — революция в образовательных технологиях*

</div>

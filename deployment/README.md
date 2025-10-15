# 🚀 Deployment Guide - EduGPT KZ

## 📋 Обзор развертывания

Это руководство описывает процесс развертывания EduGPT KZ в различных средах.

## 🎯 Требования к системе

### Минимальные требования
- **CPU:** 2 cores, 2.4 GHz
- **RAM:** 4 GB
- **Storage:** 50 GB SSD
- **OS:** Ubuntu 20.04+ или CentOS 8+

### Рекомендуемые требования
- **CPU:** 4+ cores, 3.0+ GHz
- **RAM:** 8+ GB
- **Storage:** 100+ GB NVMe SSD
- **Network:** 1 Gbps

## 🐳 Docker Deployment

### 1. Подготовка окружения
```bash
# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Конфигурация
```bash
# Клонирование репозитория
git clone https://github.com/kuralbekadilet475/EduGPT-KZ.git
cd EduGPT-KZ

# Создание .env файла
cp .env.example .env
# Отредактируйте .env с вашими настройками
```

### 3. Запуск сервисов
```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### 4. Инициализация базы данных
```bash
# Создание таблиц
docker-compose exec backend python scripts/init_db.py

# Загрузка демо данных
docker-compose exec backend python scripts/load_demo_data.py
```

## ☁️ Production Deployment

### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y nginx certbot python3-certbot-nginx ufw

# Настройка firewall
sudo ufw allow 22,80,443/tcp
sudo ufw enable
```

### 2. Настройка PostgreSQL
```bash
# Установка PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Создание пользователя и базы
sudo -u postgres psql
CREATE USER edugpt_user WITH PASSWORD 'secure_password';
CREATE DATABASE edugpt_kz OWNER edugpt_user;
GRANT ALL PRIVILEGES ON DATABASE edugpt_kz TO edugpt_user;
\q
```

### 3. Настройка Redis
```bash
# Установка Redis
sudo apt install -y redis-server

# Конфигурация Redis
sudo nano /etc/redis/redis.conf
# Установите: requirepass your_redis_password
sudo systemctl restart redis
```

### 4. Развертывание приложения
```bash
# Создание пользователя для приложения
sudo useradd -m -s /bin/bash edugpt
sudo usermod -aG docker edugpt

# Переключение на пользователя
sudo su - edugpt

# Клонирование репозитория
git clone https://github.com/kuralbekadilet475/EduGPT-KZ.git
cd EduGPT-KZ

# Настройка production окружения
cp .env.production .env
# Отредактируйте .env с production настройками
```

### 5. Настройка Nginx
```nginx
# /etc/nginx/sites-available/edugpt
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin Panel
    location /admin/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/edugpt/EduGPT-KZ/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 6. SSL сертификат
```bash
# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 Systemd Services

### 1. Backend Service
```ini
# /etc/systemd/system/edugpt-backend.service
[Unit]
Description=EduGPT Backend API
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=edugpt
Group=edugpt
WorkingDirectory=/home/edugpt/EduGPT-KZ
Environment=PATH=/home/edugpt/EduGPT-KZ/venv/bin
ExecStart=/home/edugpt/EduGPT-KZ/venv/bin/python backend/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Bot Service
```ini
# /etc/systemd/system/edugpt-bot.service
[Unit]
Description=EduGPT Telegram Bot
After=network.target edugpt-backend.service

[Service]
Type=exec
User=edugpt
Group=edugpt
WorkingDirectory=/home/edugpt/EduGPT-KZ
Environment=PATH=/home/edugpt/EduGPT-KZ/venv/bin
ExecStart=/home/edugpt/EduGPT-KZ/venv/bin/python run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Активация сервисов
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Запуск сервисов
sudo systemctl enable edugpt-backend
sudo systemctl enable edugpt-bot
sudo systemctl start edugpt-backend
sudo systemctl start edugpt-bot

# Проверка статуса
sudo systemctl status edugpt-backend
sudo systemctl status edugpt-bot
```

## 📊 Мониторинг и логирование

### 1. Настройка логирования
```bash
# Создание директорий для логов
sudo mkdir -p /var/log/edugpt
sudo chown edugpt:edugpt /var/log/edugpt

# Настройка logrotate
sudo nano /etc/logrotate.d/edugpt
```

### 2. Мониторинг с Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'edugpt-backend'
    static_configs:
      - targets: ['localhost:8000']

  - job_name: 'edugpt-bot'
    static_configs:
      - targets: ['localhost:8001']
```

### 3. Grafana Dashboard
```bash
# Запуск Grafana
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana

# Импорт дашбордов
# Используйте файлы из infra/docker/grafana/dashboards/
```

## 🔄 CI/CD Pipeline

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /home/edugpt/EduGPT-KZ
            git pull origin main
            docker-compose down
            docker-compose build
            docker-compose up -d
```

### 2. Автоматическое развертывание
```bash
# Скрипт развертывания
#!/bin/bash
# deploy.sh

set -e

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python scripts/migrate.py

# Restart services
sudo systemctl restart edugpt-backend
sudo systemctl restart edugpt-bot

# Health check
curl -f http://localhost:8000/api/health || exit 1

echo "✅ Deployment completed successfully!"
```

## 🛡️ Безопасность

### 1. Настройка firewall
```bash
# UFW configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. Fail2ban
```bash
# Установка fail2ban
sudo apt install -y fail2ban

# Конфигурация
sudo nano /etc/fail2ban/jail.local
```

### 3. Backup стратегия
```bash
# Автоматический backup
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/edugpt"

# Database backup
pg_dump edugpt_kz > "$BACKUP_DIR/db_$DATE.sql"

# Files backup
tar -czf "$BACKUP_DIR/files_$DATE.tar.gz" /home/edugpt/EduGPT-KZ

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 📈 Масштабирование

### 1. Горизонтальное масштабирование
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  backend:
    image: edugpt/backend:latest
    deploy:
      replicas: 3
    environment:
      - WORKER_PROCESSES=4

  bot:
    image: edugpt/bot:latest
    deploy:
      replicas: 2
```

### 2. Load Balancer
```nginx
# nginx.conf для load balancing
upstream backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

## 🔧 Troubleshooting

### Частые проблемы

1. **База данных не подключается**
```bash
# Проверка подключения
psql -h localhost -U edugpt_user -d edugpt_kz

# Проверка статуса PostgreSQL
sudo systemctl status postgresql
```

2. **Redis недоступен**
```bash
# Проверка Redis
redis-cli ping

# Проверка конфигурации
sudo nano /etc/redis/redis.conf
```

3. **Bot не отвечает**
```bash
# Проверка логов
sudo journalctl -u edugpt-bot -f

# Проверка токена
curl -X GET "https://api.telegram.org/bot<TOKEN>/getMe"
```

---

*Полное руководство по развертыванию доступно в коммерческой версии с дополнительными конфигурациями и автоматизацией.*

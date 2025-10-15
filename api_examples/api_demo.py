#!/usr/bin/env python3
"""
EduGPT KZ - API Demo Examples
Автор: Adilet Kuralbek
© 2025. All rights reserved.

ДЕМОНСТРАЦИОННЫЕ ПРИМЕРЫ API
Этот файл содержит примеры использования API EduGPT KZ.
Полная документация API доступна в коммерческой лицензии.
"""

import requests
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime

class EduGPTAPIDemo:
    """Демонстрационный клиент API EduGPT KZ"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "EduGPT-Demo-Client/1.0"
        }
    
    def health_check(self) -> Dict:
        """Проверка состояния API"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            return {
                "status": "success",
                "data": response.json(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "status_code": 0
            }
    
    def send_message(self, message: str, user_id: int, language: str = "ru") -> Dict:
        """Отправка сообщения боту"""
        payload = {
            "message": message,
            "user_id": user_id,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/message",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            return {
                "status": "success",
                "data": response.json(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "status_code": 0
            }
    
    def search_faq(self, query: str, language: str = "ru") -> Dict:
        """Поиск в FAQ базе"""
        params = {
            "query": query,
            "language": language,
            "limit": 5
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/faq/search",
                params=params,
                headers=self.headers,
                timeout=5
            )
            
            return {
                "status": "success",
                "data": response.json(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "status_code": 0
            }
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/stats",
                headers=self.headers,
                timeout=5
            )
            
            return {
                "status": "success",
                "data": response.json(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "status_code": 0
            }
    
    async def async_send_message(self, session: aiohttp.ClientSession, 
                               message: str, user_id: int, language: str = "ru") -> Dict:
        """Асинхронная отправка сообщения"""
        payload = {
            "message": message,
            "user_id": user_id,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            async with session.post(
                f"{self.base_url}/api/chat/message",
                json=payload,
                headers=self.headers
            ) as response:
                data = await response.json()
                return {
                    "status": "success",
                    "data": data,
                    "status_code": response.status
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "status_code": 0
            }

def demo_sync_api():
    """Демонстрация синхронного API"""
    print("🔄 Демонстрация синхронного API")
    print("=" * 40)
    
    api = EduGPTAPIDemo()
    
    # 1. Проверка здоровья
    print("1. Проверка состояния API...")
    health = api.health_check()
    print(f"   Результат: {health}")
    
    # 2. Поиск в FAQ
    print("\n2. Поиск в FAQ...")
    faq_result = api.search_faq("расписание", "ru")
    print(f"   Результат: {faq_result}")
    
    # 3. Отправка сообщения
    print("\n3. Отправка сообщения...")
    message_result = api.send_message("Когда экзамен по математике?", 12345, "ru")
    print(f"   Результат: {message_result}")
    
    # 4. Получение статистики
    print("\n4. Получение статистики...")
    stats = api.get_stats()
    print(f"   Результат: {stats}")

async def demo_async_api():
    """Демонстрация асинхронного API"""
    print("\n⚡ Демонстрация асинхронного API")
    print("=" * 40)
    
    api = EduGPTAPIDemo()
    
    async with aiohttp.ClientSession() as session:
        # Множественные запросы одновременно
        tasks = []
        
        messages = [
            ("Когда экзамен по математике?", 12345),
            ("Где мое расписание?", 12346),
            ("Сколько стипендия?", 12347),
            ("Контакты приемной комиссии", 12348),
            ("Как добавить FAQ?", 12349)
        ]
        
        print("Отправляем 5 сообщений одновременно...")
        
        for message, user_id in messages:
            task = api.async_send_message(session, message, user_id)
            tasks.append(task)
        
        # Ждем все результаты
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            print(f"   Сообщение {i+1}: {result}")

def demo_api_examples():
    """Демонстрация различных примеров API"""
    print("\n📚 Примеры использования API")
    print("=" * 40)
    
    api = EduGPTAPIDemo()
    
    # Примеры запросов
    examples = [
        {
            "name": "FAQ поиск на русском",
            "method": "GET",
            "endpoint": "/api/faq/search",
            "params": {"query": "расписание", "language": "ru"},
            "description": "Поиск информации о расписании"
        },
        {
            "name": "FAQ поиск на казахском",
            "method": "GET", 
            "endpoint": "/api/faq/search",
            "params": {"query": "сабақ кестесі", "language": "kk"},
            "description": "Поиск информации о расписании на казахском"
        },
        {
            "name": "Отправка сообщения студенту",
            "method": "POST",
            "endpoint": "/api/chat/message",
            "body": {
                "message": "Когда экзамен по программированию?",
                "user_id": 12345,
                "language": "ru"
            },
            "description": "Отправка сообщения от студента"
        },
        {
            "name": "Отправка сообщения преподавателю",
            "method": "POST",
            "endpoint": "/api/chat/message", 
            "body": {
                "message": "Как добавить новый FAQ?",
                "user_id": 54321,
                "language": "ru",
                "is_teacher": True
            },
            "description": "Отправка сообщения от преподавателя"
        },
        {
            "name": "Получение статистики",
            "method": "GET",
            "endpoint": "/api/analytics/stats",
            "description": "Получение общей статистики системы"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Метод: {example['method']}")
        print(f"   Endpoint: {example['endpoint']}")
        if 'params' in example:
            print(f"   Параметры: {example['params']}")
        if 'body' in example:
            print(f"   Тело запроса: {example['body']}")
        print(f"   Описание: {example['description']}")

def demo_curl_examples():
    """Примеры curl команд"""
    print("\n🔧 Примеры curl команд")
    print("=" * 40)
    
    curl_examples = [
        {
            "name": "Проверка здоровья API",
            "command": "curl -X GET http://localhost:8000/api/health"
        },
        {
            "name": "Поиск в FAQ",
            "command": "curl -X GET 'http://localhost:8000/api/faq/search?query=расписание&language=ru'"
        },
        {
            "name": "Отправка сообщения",
            "command": """curl -X POST http://localhost:8000/api/chat/message \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Когда экзамен?", "user_id": 12345, "language": "ru"}'"""
        },
        {
            "name": "Получение статистики",
            "command": "curl -X GET http://localhost:8000/api/analytics/stats"
        }
    ]
    
    for i, example in enumerate(curl_examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   {example['command']}")

async def main():
    """Главная функция демонстрации"""
    print("🎓 EduGPT KZ - API Demo Examples")
    print("Автор: Adilet Kuralbek")
    print("© 2025. All rights reserved.")
    print("📧 kuralbekadilet475@gmail.com")
    print("\n" + "="*50)
    
    # Демонстрации
    demo_sync_api()
    await demo_async_api()
    demo_api_examples()
    demo_curl_examples()
    
    print("\n" + "="*50)
    print("✅ Демонстрация завершена!")
    print("📚 Полная документация API доступна в коммерческой версии")

if __name__ == "__main__":
    print("⚖️ ДЕМОНСТРАЦИОННАЯ ВЕРСИЯ API")
    print("© 2025 Adilet Kuralbek. All rights reserved.")
    print("🚫 Коммерческое использование запрещено без лицензии\n")
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Ошибка демонстрации: {e}")

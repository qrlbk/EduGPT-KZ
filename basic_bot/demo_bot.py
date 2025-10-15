#!/usr/bin/env python3
"""
EduGPT KZ - Demo Bot
Автор: Adilet Kuralbek
© 2025. All rights reserved.

ДЕМОНСТРАЦИОННАЯ ВЕРСИЯ
Этот файл содержит упрощенную реализацию бота для демонстрации возможностей.
Полная версия доступна в коммерческой лицензии.
"""

import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class User:
    """Модель пользователя"""
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    language: str = "ru"
    is_student: bool = True

@dataclass
class Message:
    """Модель сообщения"""
    text: str
    user_id: int
    timestamp: datetime
    language: str = "ru"

class SimpleFAQ:
    """Простая система FAQ для демо"""
    
    def __init__(self):
        self.faq_data = {
            "ru": {
                "расписание": "Расписание занятий доступно в личном кабинете e.edugpt.edu.kz в разделе 'Расписание'",
                "экзамен": "Расписание экзаменов публикуется за 2 недели до начала сессии на сайте университета",
                "стипендия": "Стипендия выплачивается 10 числа каждого месяца. Размер: 50,000 тенге",
                "контакты": "Приемная комиссия: +7 (727) 377-33-33, email: info@edugpt.edu.kz",
                "админ": "Для добавления FAQ используйте команду /faq_add в админ-панели"
            },
            "kk": {
                "сабақ кестесі": "Сабақ кестесі e.edugpt.edu.kz сайтындағы жеке кабинетте 'Сабақ кестесі' бөлімінде",
                "емтихан": "Емтихан кестесі сессия басталмас бұрын 2 апта бұрын университет сайтында жарияланады",
                "стипендия": "Стипендия әр айдың 10-ында төленеді. Мөлшері: 50,000 теңге",
                "байланыс": "Қабылдау комиссиясы: +7 (727) 377-33-33, email: info@edugpt.edu.kz"
            }
        }

    def search(self, query: str, language: str = "ru") -> Optional[str]:
        """Поиск в FAQ базе"""
        query_lower = query.lower().strip()
        
        for key, answer in self.faq_data.get(language, {}).items():
            if key in query_lower:
                return answer
        
        return None

class DemoEduGPTBot:
    """Демонстрационный бот EduGPT KZ"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.faq = SimpleFAQ()
        self.stats = {
            "total_messages": 0,
            "users_count": 0,
            "faq_hits": 0
        }
        
    async def start(self):
        """Запуск бота"""
        logger.info("🚀 EduGPT KZ Demo Bot запущен!")
        logger.info("📧 Автор: Adilet Kuralbek (kuralbekadilet475@gmail.com)")
        logger.info("⚖️ © 2025. All rights reserved.")
        print("\n" + "="*50)
        print("🎓 EduGPT KZ - AI Assistant Demo")
        print("="*50)
        print("Добро пожаловать в демонстрационную версию!")
        print("Введите 'quit' для выхода\n")
        
        await self.run_demo()

    async def process_message(self, user_id: int, text: str) -> str:
        """Обработка сообщения пользователя"""
        # Обновляем статистику
        self.stats["total_messages"] += 1
        
        # Получаем или создаем пользователя
        if user_id not in self.users:
            self.users[user_id] = User(id=user_id)
            self.stats["users_count"] += 1
        
        user = self.users[user_id]
        user.language = self.detect_language(text)
        
        # Специальные команды
        if text.lower().startswith('/'):
            return await self.handle_command(user, text)
        
        # Поиск в FAQ
        faq_answer = self.faq.search(text, user.language)
        if faq_answer:
            self.stats["faq_hits"] += 1
            return faq_answer
        
        # Общий ответ
        return self.get_general_response(text, user.language)

    def detect_language(self, text: str) -> str:
        """Определение языка текста (упрощенная версия)"""
        kazakh_indicators = ['қ', 'ә', 'ө', 'ұ', 'ү', 'і', 'ң', 'ғ']
        if any(char in text.lower() for char in kazakh_indicators):
            return "kk"
        return "ru"

    async def handle_command(self, user: User, text: str) -> str:
        """Обработка команд"""
        command = text.lower().strip()
        
        if command == '/start':
            return self.get_welcome_message(user.language)
        elif command == '/help':
            return self.get_help_message(user.language)
        elif command == '/stats':
            return self.get_stats_message()
        elif command == '/faq':
            return self.get_faq_topics(user.language)
        else:
            return "❓ Неизвестная команда. Используйте /help для справки."

    def get_welcome_message(self, language: str) -> str:
        """Приветственное сообщение"""
        if language == "kk":
            return """🎓 Сәлем! Мен EduGPT KZ ботымын!

Мен сізге көмектесе аламын:
• Сабақ кестесін табу
• Емтихан туралы ақпарат
• Стипендия туралы сұрақтар
• Байланыс мәліметтері

Сұрақ қойыңыз! 🤖"""
        else:
            return """🎓 Привет! Я EduGPT KZ бот!

Я могу помочь вам с:
• Расписанием занятий
• Информацией об экзаменах  
• Вопросами по стипендии
• Контактными данными

Задавайте вопросы! 🤖"""

    def get_help_message(self, language: str) -> str:
        """Справочное сообщение"""
        if language == "kk":
            return """📚 Көмек:

🔍 Сұрақтар мысалдары:
• "Сабақ кестем қайда?"
• "Емтихан қашан?"
• "Стипендия қанша?"

📋 Командалар:
/start - бастау
/help - көмек
/stats - статистика
/faq - жиі қойылатын сұрақтар"""
        else:
            return """📚 Справка:

🔍 Примеры вопросов:
• "Где мое расписание?"
• "Когда экзамен?"
• "Сколько стипендия?"

📋 Команды:
/start - начать
/help - справка
/stats - статистика
/faq - частые вопросы"""

    def get_stats_message(self) -> str:
        """Сообщение со статистикой"""
        return f"""📊 Статистика демо-бота:

👥 Пользователей: {self.stats['users_count']}
💬 Сообщений: {self.stats['total_messages']}
🎯 FAQ попаданий: {self.stats['faq_hits']}

📈 Точность ответов: {self.stats['faq_hits'] / max(self.stats['total_messages'], 1) * 100:.1f}%"""

    def get_faq_topics(self, language: str) -> str:
        """Список тем FAQ"""
        if language == "kk":
            return """❓ Жиі қойылатын сұрақтар:

• Сабақ кестесі
• Емтихан
• Стипендия
• Байланыс мәліметтері

Сұрақтың бірін жазып жіберіңіз!"""
        else:
            return """❓ Часто задаваемые вопросы:

• Расписание занятий
• Экзамены
• Стипендия
• Контактная информация

Напишите один из вопросов!"""

    def get_general_response(self, text: str, language: str) -> str:
        """Общий ответ на неизвестные вопросы"""
        if language == "kk":
            return """🤔 Кешіріңіз, мен бұл сұраққа дәл жауап бере алмаймын.

Қайталап сұраңыз немесе /faq командасын қолданыңыз.
Көмек керек болса, қабылдау комиссиясына хабарласыңыз:
📞 +7 (727) 377-33-33"""
        else:
            return """🤔 Извините, я не могу дать точный ответ на этот вопрос.

Переформулируйте вопрос или используйте команду /faq.
Если нужна помощь, обратитесь в приемную комиссию:
📞 +7 (727) 377-33-33"""

    async def run_demo(self):
        """Запуск демонстрационного режима"""
        user_id = 1  # Демо пользователь
        
        while True:
            try:
                # Получаем ввод пользователя
                user_input = input("\n👤 Вы: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'выход']:
                    print("\n👋 До свидания! Спасибо за использование EduGPT KZ!")
                    break
                
                if not user_input:
                    continue
                
                # Обрабатываем сообщение
                response = await self.process_message(user_id, user_input)
                
                # Выводим ответ
                print(f"\n🤖 EduGPT: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Демо завершено. До свидания!")
                break
            except Exception as e:
                logger.error(f"Ошибка в демо: {e}")
                print("❌ Произошла ошибка. Попробуйте еще раз.")

async def main():
    """Главная функция"""
    bot = DemoEduGPTBot()
    await bot.start()

if __name__ == "__main__":
    # Проверка лицензии
    print("⚖️ ДЕМОНСТРАЦИОННАЯ ВЕРСИЯ")
    print("© 2025 Adilet Kuralbek. All rights reserved.")
    print("📧 Контакты: kuralbekadilet475@gmail.com")
    print("🚫 Коммерческое использование запрещено без лицензии\n")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print("❌ Критическая ошибка. Демо недоступно.")

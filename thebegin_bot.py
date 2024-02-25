#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from telegram import Update
from telegram.ext import PicklePersistence, Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from fuzzywuzzy import fuzz
import logging

logging.basicConfig(
    filename='/app/bot.log',  # Путь к файлу логов
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

TOKEN = os.environ.get('YOUR_TELEGRAM_TOKEN')
if TOKEN is None:
    print("Не найден токен бота. Убедитесь, что переменная окружения YOUR_TELEGRAM_TOKEN установлена.")
    sys.exit(1)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id, 'Привет, малюск')

def help_command(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id, 'Это ваш бот. Доступные команды:\n/start - начать диалог\n/help - получить справку')

def how_are_you(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    expected_phrases = ["как дела?", "как дила?"]
    best_match, score = max(((phrase, fuzz.ratio(user_message, phrase)) for phrase in expected_phrases), key=lambda x: x[1])

    if score >= 80:
        context.bot.send_message(update.message.chat_id, f'Спасибо, что спросил! У меня всё отлично. А у тебя как дела?')
        logging.info(f"Received '{best_match}' message")
    else:
        context.bot.send_message(update.message.chat_id, 'Извините, не понял вас. Можете переформулировать вопрос?')

def what_are_you_doing(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id, 'Я занят общением с вами! Чем могу помочь?')

def main():
    persistence = PicklePersistence('/app/conversation_data.pkl')
    updater = Updater(TOKEN, use_context=True, persistence=persistence)

    # Добавленные строки
    PORT = int(os.environ.get('PORT', 5000))
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.setWebhook(f"https://fierce-anchorage-81100-390a3927338e.herokuapp.com/{TOKEN}")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.regex(r'как дела\??') | Filters.regex(r'как дила\??'), how_are_you))
    dp.add_handler(MessageHandler(Filters.regex(r'что ты делаешь\??'), what_are_you_doing))

    logging.info("Bot started")

    updater.idle()

if __name__ == '__main__':
    main()

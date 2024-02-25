#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import PicklePersistence, Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from fuzzywuzzy import fuzz
import logging

logging.basicConfig(
    filename='/app/bot.log',  # Путь к файлу логов
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

TOKEN = '6819081129:AAGpDpi1c4UP4Duis0JGsK2vamaEcLg0b5Q'

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
    persistence = PickleP

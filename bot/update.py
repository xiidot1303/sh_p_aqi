from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    InlineQueryHandler
)
from config import TELEGRAM_BOT_API_TOKEN, DEBUG
from bot.main import *

persistence = PicklePersistence(filename="persistencebot")

bot_obj = Bot(TELEGRAM_BOT_API_TOKEN)

if not DEBUG:  # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=10, use_context=True, persistence=persistence)

else:  # in development
    updater = Updater(
        token=TELEGRAM_BOT_API_TOKEN, workers=10, use_context=True, persistence=persistence,
    )
    dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.voice, get_voice))
dp.add_handler(MessageHandler(Filters.text, set_title))
dp.add_handler(InlineQueryHandler(search))
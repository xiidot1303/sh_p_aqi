from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from telegram import Update
from bot.update import dp, updater
import json
from django.views.decorators.csrf import csrf_exempt
from config import TELEGRAM_BOT_API_TOKEN, DEBUG
from app.models import *

@csrf_exempt
def bot_webhook(request):

    if DEBUG:
        updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode('utf-8')), dp.bot)
        dp.process_update(update)
    return HttpResponse('Bot started!')

def get_voice_file(request, voice_id):
    voice_obj = Voice.objects.get(pk=voice_id)
    f = open('files/{}'.format(voice_obj.file), 'rb')  
    return FileResponse(f)
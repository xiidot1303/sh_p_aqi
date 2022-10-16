from app.models import *
from django.db.models import Q
from telegram import (
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultVoice,
    InlineQueryResultCachedVoice,
    InputInvoiceMessageContent,
    InputMediaAudio,
    InputTextMessageContent,
    InputMediaPhoto,
    Audio
)
from transliterate import translit
from uuid import uuid4

def get_voice(update, context):
    print(update)
    bot = context.bot
    voice_id = bot.getFile(update.message.voice.file_id)
    *args, file_name = str(voice_id.file_path).split('/')
    d_voice = voice_id.download('files/voices/{}'.format(file_name))
    file_obj = str(d_voice).replace('files/', '')
    Voice.objects.create(
        file = file_obj,
        file_id = update.message.voice.file_id,
        msg_id = update.message.message_id,
        )
    return 

def set_title(update, context):
    if not update.message.reply_to_message:
        update.message.reply_text('empty')
        return
    
    msg_id = update.message.reply_to_message.message_id
    try:
        voice_obj = Voice.objects.get(msg_id=msg_id)
    except:
        update.message.reply_text('voice not found')
    voice_obj.title = update.message.text
    voice_obj.save()
    update.message.reply_text('title set:\n\n{}'.format(update.message.text))
    return

def search(update, context):
    text = update.inline_query.query
    text_ru = translit(text, 'ru')
    try:
        text_en = translit(text, reversed=True)
    except:
        text_en = text

    text_en = regexing_en(text_en)
    text_ru = regexing_ru(text_ru)

    voices = Voice.objects.filter(
        Q(title__iregex=text_en) | Q(title__iregex=text_ru) | Q(title__icontains=text)
    )

    article = [
        InlineQueryResultVoice(
            id=str(uuid4()),
            voice_url = voice.file_id,
            title=voice.title,
            # input_message_content=InputMediaAudio(voice.file),
            # input_message_content=InputTextMessageContent('error')
        )
        for voice in voices
    ]

    if not article:
        article = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title='not found',
                input_message_content=InputTextMessageContent('not found')
            )
        ]

    update.inline_query.answer(article, auto_pagination=True)


def regexing_en(text):
    list_couples = [
        'ao', 'xh', 'ie', 'qk', 'cs', 'jy'
    ]

    for i in list_couples:
        text = text.replace(i[0], f'({i[0]}|{i[1]})')
        text = text.replace(i[1], f'({i[0]}|{i[1]})')
        text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

    return text

def regexing_ru(text):
    list_couples = [
        'ао', 'её', 'ыи', 'юу', 'щш'
    ]

    for i in list_couples:
        text = text.replace(i[0], f'({i[0]}|{i[1]})')
        text = text.replace(i[1], f'({i[0]}|{i[1]})')
        text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

    return text
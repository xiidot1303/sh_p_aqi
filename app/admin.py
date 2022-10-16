from django.contrib import admin
from app.models import *

class VoiceAdmin(admin.ModelAdmin):
    list_display = ['msg_id', 'title']

admin.site.register(Voice, VoiceAdmin)
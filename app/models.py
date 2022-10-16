from django.db import models

class Voice(models.Model):
    file = models.FileField(null=True, blank=False, upload_to='voices')
    file_id = models.CharField(null=True, blank=False, max_length=64)
    msg_id = models.IntegerField(null=True, blank=False)
    title = models.CharField(null=True, blank=True, max_length=255)

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.
class Message(models.Model):
    sender          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content         = RichTextField()
    timestamp       = models.DateTimeField(auto_now_add=True)
    read            = models.BooleanField(default=False)
    modified_date   = models.DateTimeField(auto_now=True)
    receiver_name   = models.TextField()
    email           = models.EmailField()
    feedback        = models.TextField()
   
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"

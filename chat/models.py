from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)











from django.db import models

# Create your models here.

class New(models.Model):
    identification_code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=50)
    news_date= models.CharField(max_length=11)
    speaker_or_source = models.CharField(max_length=20)
    half_description = models.TextField(max_length=100)
    full_description = models.TextField(max_length=5000)
    news_picture = models.FileField(upload_to="news_picture")

    def __str__(self):
        return f"{self.identification_code},{self.title},{self.news_date}," \
            f"{self.speaker_or_source},{self.half_description},{self.full_description},{self.news_picture}"

class Event(models.Model):
    identification_code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=50)
    event_day= models.CharField(max_length=2)
    event_month = models.CharField(max_length=3)
    event_time = models.CharField(max_length=15)
    event_venue = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    event_picture = models.FileField(upload_to="events_picture")

    def __str__(self):
        return f"{self.identification_code},{self.title},{self.event_day},{self.event_month},{self.event_time},{self.event_venue},{self.description},{self.event_picture}"


from django.contrib import admin
from chat.models import Message

# Register your models here.
admin.site.register(Message)






from .models import New,Event

class tc1(admin.ModelAdmin):
    list_display = ("identification_code","title", "news_date","title","speaker_or_source","half_description","news_picture",)
    list_filter = ("title",)


class tc2(admin.ModelAdmin):
    list_display = ("identification_code","title", "event_day","event_month","event_time","event_venue","description","event_picture",)
    list_filter = ("title",)



admin.site.register(New,tc1)
admin.site.register(Event,tc2)

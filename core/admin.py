from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Question)
class QustionAdmin(admin.ModelAdmin):
    list_display = ['user','topic','slug','date_posted']
    

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user','question']

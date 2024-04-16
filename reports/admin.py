from django.contrib import admin
from .models import Report

@admin.register(Report)
class UnPayedReportsPanel (admin.ModelAdmin) :
    list_display = ('user','gamia','date',)


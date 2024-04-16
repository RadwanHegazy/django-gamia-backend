from django.contrib import admin
from .models import Gamia, GamiaUser

@admin.register(Gamia)
class GaminPanel (admin.ModelAdmin) :
    list_display = ('owner','started_at','end_at','id',)

@admin.register(GamiaUser)
class GaminUserPanel (admin.ModelAdmin) :
    list_display = ('user','gamia','recived_money_at','enter_at',)



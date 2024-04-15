from django.contrib import admin
from .models import Payment, Withdraw


@admin.register(Payment)
class PaymentPanel(admin.ModelAdmin) :
    list_display = ('user','amount','status','isExpired')

@admin.register(Withdraw)
class WithdrawPanel(admin.ModelAdmin) :
    list_display = ('user','amount','mobile_cash','date',)
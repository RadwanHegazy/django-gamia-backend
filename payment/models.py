from django.db import models
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

PAY_STATUS = (
    ('success','success'),
    ('cancel','cancel'),
)

class Payment (models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    isExpired = models.BooleanField(default=False)
    status = models.CharField(choices=PAY_STATUS,max_length=20,null=True,blank=True)
    user = models.ForeignKey('users.User',related_name='user_pay',on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.user.full_name
    

class Withdraw(models.Model): 
    user = models.ForeignKey('users.User',related_name='user_withdraw',on_delete=models.SET_NULL,null=True)
    mobile_cash = PhoneNumberField()
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) : 
        return self.user.full_name
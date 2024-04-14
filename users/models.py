from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class Managers (BaseUserManager) : 
    
    def create_user(self,**data) : 
        password = data.pop('password')
        user = self.model(**data)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,**data):
        data['is_superuser'] = True
        data['is_staff'] = True
        return self.create_user(**data)
    

class User (AbstractUser) : 
    objects = Managers()
    
    # discard fields
    username = None
    first_name = None
    last_name = None
    groups = None
    user_permissions = None


    # addition fields
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=225)
    cash_phone = PhoneNumberField(unique=True)
    picture = models.ImageField(upload_to='user-pics/',default='user.png')
    balance = models.FloatField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name',)

    def __str__(self) -> str:
        return self.full_name
    

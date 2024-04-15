from rest_framework import serializers
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

    

class RegisterSerializer(serializers.ModelSerializer) : 
    
    class Meta:
        model = User
        fields = ('id','full_name','email','password','cash_phone','picture')

    
    def validate(self, attrs):
        password = attrs['password']
        validate_password(password)
        return attrs
    
    def save(self, **kwargs):
        self.user = User.objects.create_user(**self.validated_data)
        self.user.save()
        return self.user
    
    @property
    def tokens (self):
        jwt_tokens = RefreshToken.for_user(self.user)
        data = {
            'refresh' : str(jwt_tokens),
            'access' : str(jwt_tokens.access_token),
        } 
        return data
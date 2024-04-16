
from rest_framework import serializers
from gamia.models import Gamia, GamiaUser
from users.models import User

class CreateGamiaSerialzier (serializers.ModelSerializer) : 
    class Meta:
        model = Gamia
        fields = ('id','max_users_count','price_per_user','pay_every_days',)

    
    def save(self, **kwargs):
        data = self.validated_data
        data['total'] = (
            self.validated_data['max_users_count'] * 
            self.validated_data['price_per_user']
            )
        data['owner'] = self.context['user']

        return super().save(**data)

class GamiaUserSerializer(serializers.ModelSerializer) : 
    class Meta:
        model = GamiaUser
        fields = ('user','recived_money_at','hasReceived',)

    @staticmethod
    def user_details (user_id) : 
        user = User.objects.get(id=user_id)
        return {
            'full_name' : user.full_name,
            'picture' : user.picture.url,
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = self.user_details(data['user'])    
        return data
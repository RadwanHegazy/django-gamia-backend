
from rest_framework import serializers
from gamia.models import Gamia


class CreateGamiaSerialzier (serializers.ModelSerializer) : 
    class Meta:
        model = Gamia
        fields = ('id','max_users_count','price_per_user','pay_every_days',)

    
    def save(self, **kwargs):
        data = self.validated_data
        data['total'] = (
            self.validated_data['max_users_count'] * 
            self.validated_data['price_per_user'] * 
            self.validated_data['pay_every_days']
            )
        data['owner'] = self.context['user']

        return super().save(**data)
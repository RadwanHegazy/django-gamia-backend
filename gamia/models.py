from django.db import models
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save

class Gamia (models.Model) : 
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    owner = models.ForeignKey('users.User',related_name='user_gamia_owner',on_delete=models.CASCADE)
    title = models.CharField(max_length=500,null=True,blank=True)
    current_balance = models.FloatField(default=0)
    started_at = models.DateField(null=True)
    end_at = models.DateField(null=True)
    max_users_count = models.PositiveIntegerField()
    price_per_user = models.FloatField()
    pay_every_days = models.PositiveIntegerField()
    total = models.FloatField()

    def __str__(self) -> str:
        return self.title
    
    def save(self,**kwargs):
        if self.title is None : 
            self.title = f"الجمعية الخاصة ب : {self.owner.full_name}"
        
        
        super().save(**kwargs)

    

class GamiaUser (models.Model) : 
    user = models.ForeignKey('users.User',related_name='user_gamia',on_delete=models.CASCADE)
    gamia = models.ForeignKey(Gamia,related_name='gamia_group',on_delete=models.CASCADE)
    enter_at = models.DateTimeField(auto_now_add=True)
    recived_money_at = models.DateField(null=True,blank=True)
    hasReceived = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.user.full_name} | {self.gamia.title}"

    class Meta:
        ordering = ('enter_at',)    


@receiver(post_save,sender=Gamia)
def CreateCustomGamiaUser(created, instance:Gamia,**kwargs) :
    if created :
        g = GamiaUser.objects.create(
            gamia = instance,
            user = instance.owner,
        )
        g.save()

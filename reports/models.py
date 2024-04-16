from django.db import models
from gamia.models import Gamia

class Report (models.Model) : 
    body = models.TextField()
    user = models.ForeignKey('users.User',related_name='report_for_user',on_delete=models.SET_NULL,null=True,editable=False)
    gamia = models.ForeignKey(Gamia,related_name='report_for_gamia',on_delete=models.SET_NULL,null=True,editable=False)
    date = models.DateField(auto_now_add=True)


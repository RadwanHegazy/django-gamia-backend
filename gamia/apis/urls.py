from django.urls import path
from .views import create, get


urlpatterns = [
    path('create/',create.CreateGamia.as_view(),name='create_gamia'),
    path('get/',get.GetAllUserGamia.as_view(),name='get_gamia'),
    path('get/<str:gamia_id>/',get.GetGamia.as_view(),name='get_gamia_group'),
]
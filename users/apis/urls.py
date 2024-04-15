from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import profile, register
from .payment_views import charge, withdraw


urlpatterns = [
    path('auth/login/',TokenObtainPairView.as_view(),name='login'),
    path('auth/register/',register.RegisterView.as_view(),name='register'),
    path('profile/',profile.ProfileView.as_view(),name='profile'),
    path('charge/',charge.ChargeView.as_view(),name='charge'),
    path('withdraw/',withdraw.WithdrawView.as_view(),name='withdraw'),
]
from .views import success, cancel
from django.urls import path

urlpatterns = [
    path('<str:payment_id>/success/',success.SuccessView.as_view()),
    path('<str:payment_id>/cancel/',cancel.CancelView.as_view()),
]
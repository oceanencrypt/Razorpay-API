from .views import PaymentSuccessView, PaymentView
from django.urls import path


urlpatterns = [
    path("",  PaymentView.as_view(), name="payment"),
    path("success/",  PaymentSuccessView.as_view(), name="payment_success"),
]
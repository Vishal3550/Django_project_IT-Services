from django.urls import path
from .views import home, register, otp_verification, service_list, service_detail, service_create, service_update, service_delete, create_payment, payment_callback

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('', service_list, name='service_list'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
    path('service/new/', service_create, name='service_create'),
    path('service/<int:pk>/edit/', service_update, name='service_update'),
    path('service/<int:pk>/delete/', service_delete, name='service_delete'),
    path('service/<int:pk>/payment/', create_payment, name='create_payment'),
    path('payment/callback/', payment_callback, name='payment_callback'),
]



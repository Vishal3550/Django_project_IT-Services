from django.core.mail import send_mail
from django.conf import settings

def send_service_created_email(service):
    subject = f'New Service Created: {service.name}'
    message = f'A new service has been created.\n\n' \
              f'Name: {service.name}\n' \
              f'Payment Terms: {service.payment_terms}\n' \
              f'Price: {service.price}\n' \
              f'Package: {service.package}\n' \
              f'Tax: {service.tax}\n' \
              f'Active: {service.active}\n'
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ['vishal843327k@gmail.com'],  # Replace with actual recipient email
        fail_silently=False,
    )

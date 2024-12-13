# Create your views here.
# services/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import Service
from .forms import ServiceForm
from .forms import UserRegistrationForm, OTPForm
from django.contrib.auth.decorators import login_required
import random
from .utils import send_service_created_email
from .razorpay_client import client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Global variable to store the OTP and the new user temporarily
otp_storage = {}

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            otp = str(random.randint(100000, 999999))
            otp_storage['otp'] = otp
            otp_storage['user'] = user
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'your_email@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('otp_verification')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def otp_verification(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == otp_storage.get('otp'):
                user = otp_storage.get('user')
                user.save()
                otp_storage.clear()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'otp_verification.html', {'form': form})


def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            send_service_created_email(service)
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})


def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})

# services/views.py
@login_required
def home(request):
    filter_status = request.GET.get('status', 'all')
    if filter_status == 'active':
        services = Service.objects.filter(active=True)
    elif filter_status == 'inactive':
        services = Service.objects.filter(active=False)
    else:
        services = Service.objects.all()
    return render(request, 'home.html', {'services': services, 'filter_status': filter_status})

@login_required
def create_payment(request, pk):
    service = get_object_or_404(Service, pk=pk)
    amount = int(service.price * 100)  # Amount in paise
    currency = 'INR'
    receipt = f'order_rcptid_{pk}'
    notes = {'service_id': service.id}

    # Create Razorpay order
    order = client.order.create(dict(amount=amount, currency=currency, receipt=receipt, notes=notes))
    service.razorpay_order_id = order['id']
    service.save()

    context = {
        'service': service,
        'order': order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,
    }
    return render(request, 'services/create_payment.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            # Fetch the service associated with this order
            service = Service.objects.get(razorpay_order_id=razorpay_order_id)
            service.razorpay_payment_id = razorpay_payment_id
            service.razorpay_payment_status = 'Paid'
            service.save()
            
            return redirect('service_detail', pk=service.pk)
        except:
            return HttpResponseBadRequest()

    return HttpResponseBadRequest()


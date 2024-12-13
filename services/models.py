from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')
    active = models.BooleanField(default=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
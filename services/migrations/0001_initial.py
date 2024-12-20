# Generated by Django 5.0.4 on 2024-07-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('payment_terms', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('package', models.CharField(max_length=100)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(upload_to='service_images/')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]

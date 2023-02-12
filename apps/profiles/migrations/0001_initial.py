# Generated by Django 3.2.7 on 2023-02-12 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False, verbose_name='primary key id')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+234980000000', max_length=20, region=None, verbose_name='Phone number')),
                ('bio', models.TextField(default='something about yourself', verbose_name='About Me')),
                ('license', models.CharField(blank=True, max_length=50, null=True, verbose_name='Real State License')),
                ('profile_photo', models.ImageField(default='/profile_default.png', upload_to='', verbose_name='Profile Photo')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=50, verbose_name='Gender')),
                ('country', django_countries.fields.CountryField(default='NG', max_length=2, verbose_name='Country')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('is_buyer', models.BooleanField(default=False, help_text='Are you looking to buy', verbose_name='IsBuyer')),
                ('is_seller', models.BooleanField(default=False, help_text='Are you looking to sell', verbose_name='IsSeller')),
                ('is_agent', models.BooleanField(default=False, help_text='Are you an agent?', verbose_name='IsAgent')),
                ('top_agent', models.BooleanField(default=False, verbose_name='TopAgent')),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Rating')),
                ('num_reveiews', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of Reveiews')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User model')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]

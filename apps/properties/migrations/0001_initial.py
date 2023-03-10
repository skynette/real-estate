# Generated by Django 3.2.7 on 2023-02-17 20:11

import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False, verbose_name='primary key id')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Property Title')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title', unique=True)),
                ('ref_code', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Property Ref Code')),
                ('description', models.TextField(blank=True, default='Default description', verbose_name='Description')),
                ('country', django_countries.fields.CountryField(blank=True, default='NG', max_length=2, verbose_name='Country')),
                ('city', models.CharField(default='Lagos', max_length=255, verbose_name='City')),
                ('postal_code', models.CharField(default='140', max_length=255, verbose_name='Postal Code')),
                ('street_address', models.CharField(default='Street Address', max_length=255, verbose_name='Street Address')),
                ('property_number', models.IntegerField(default=112, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Property Number')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price')),
                ('plot_area', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Plot Area')),
                ('bedrooms', models.IntegerField(default=1, verbose_name='bedrooms')),
                ('bathrooms', models.IntegerField(default=1, verbose_name='bathrooms')),
                ('advert_type', models.CharField(choices=[('For Sale', 'For Sale'), ('For Rent', 'For rent'), ('Auction', 'Auction')], default='For Sale', max_length=255, verbose_name='Advert Type')),
                ('property_type', models.CharField(choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Office', 'Office'), ('Warehouse', 'Warehouse'), ('Commercial', 'Commercial'), ('Other', 'Other')], default='Other', max_length=255, verbose_name='Property Type')),
                ('cover_photo', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='Main Photo')),
                ('photo1', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='Photo1')),
                ('photo2', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='photo2')),
                ('photo3', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='photo3')),
                ('photo4', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='photo4')),
                ('published_status', models.BooleanField(default=False, verbose_name='published_status')),
                ('views', models.IntegerField(default=0, verbose_name='Total views')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='agent_buyer', to=settings.AUTH_USER_MODEL, verbose_name='Agent, Seller or Buyer')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
    ]

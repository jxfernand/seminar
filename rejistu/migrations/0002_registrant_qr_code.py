# Generated by Django 5.1.6 on 2025-03-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rejistu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-15 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rejistu', '0011_alter_registrant_access_pass'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='face_encoding',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2 on 2019-04-24 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190423_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
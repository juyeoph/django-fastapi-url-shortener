# Generated by Django 4.2.23 on 2025-07-02 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shortener', '0002_url_click_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='urls', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.1.8 on 2023-05-08 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_booking_session_time_alter_booking_session_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='session_time',
            new_name='session_end_time',
        ),
        migrations.AddField(
            model_name='booking',
            name='session_start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='membership', to=settings.AUTH_USER_MODEL),
        ),
    ]

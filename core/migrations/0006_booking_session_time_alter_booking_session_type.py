# Generated by Django 4.1.8 on 2023-04-27 00:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_testimonial_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='session_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='booking',
            name='session_type',
            field=models.CharField(choices=[('private', 'Private'), ('gym', 'gym')], default='gym', max_length=10),
        ),
    ]
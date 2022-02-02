# Generated by Django 3.2.11 on 2022-02-02 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_alter_inventory_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.2.11 on 2022-02-07 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shares', '0005_auto_20220202_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryshare',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='InventoryShare', to=settings.AUTH_USER_MODEL),
        ),
    ]
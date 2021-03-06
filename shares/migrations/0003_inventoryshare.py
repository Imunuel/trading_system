# Generated by Django 3.2.11 on 2022-02-01 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shares', '0002_auto_20220131_2335'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='share', to='shares.share')),
            ],
        ),
    ]

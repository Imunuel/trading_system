# Generated by Django 3.2.11 on 2022-02-07 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0009_auto_20220202_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='buyer_offer',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='seller_offer',
        ),
    ]

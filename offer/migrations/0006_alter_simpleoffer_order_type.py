# Generated by Django 3.2.11 on 2022-01-31 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0005_auto_20220131_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleoffer',
            name='order_type',
            field=models.CharField(max_length=4),
        ),
    ]

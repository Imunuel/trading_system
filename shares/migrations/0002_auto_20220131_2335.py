# Generated by Django 3.2.11 on 2022-01-31 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='current_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='share',
            name='past_price',
            field=models.IntegerField(default=0),
        ),
    ]

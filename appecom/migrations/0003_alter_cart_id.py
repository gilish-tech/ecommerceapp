# Generated by Django 4.2.6 on 2023-10-30 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appecom', '0002_auto_20220913_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

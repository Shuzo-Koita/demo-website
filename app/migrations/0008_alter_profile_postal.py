# Generated by Django 4.0.6 on 2022-08-05 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='postal',
            field=models.IntegerField(blank=True),
        ),
    ]
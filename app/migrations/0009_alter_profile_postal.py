# Generated by Django 4.0.6 on 2022-08-05 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_profile_postal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='postal',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
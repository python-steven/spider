# Generated by Django 2.1.7 on 2019-04-19 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_partitem_trndate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partitem',
            name='USN',
        ),
        migrations.AlterField(
            model_name='partitem',
            name='TrnDate',
            field=models.DateTimeField(default='2019-03-03 11:00:00'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-06-20 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_auto_20190619_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='partitem',
            name='CreatorId',
            field=models.IntegerField(null=True),
        ),
    ]

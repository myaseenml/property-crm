# Generated by Django 4.2.6 on 2023-10-31 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_account_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_status',
            field=models.CharField(default='Block', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='new_login_ip_notification',
            field=models.CharField(default='No', max_length=255),
        ),
    ]

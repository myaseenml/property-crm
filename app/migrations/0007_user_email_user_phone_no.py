# Generated by Django 4.2.6 on 2023-11-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_availability_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='yaseenuom6@gmail.com', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no',
            field=models.CharField(default='+923029770128', max_length=20),
        ),
    ]

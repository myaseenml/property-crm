# Generated by Django 4.2.6 on 2023-10-31 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=255)),
                ('community', models.CharField(max_length=255)),
                ('property', models.CharField(max_length=255)),
                ('property_type', models.CharField(max_length=255)),
                ('floor_no', models.PositiveIntegerField()),
                ('unit_no', models.PositiveIntegerField()),
                ('bedrooms', models.PositiveIntegerField()),
                ('bathrooms', models.PositiveIntegerField()),
                ('view', models.CharField(max_length=255)),
                ('sqft', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('comments', models.CharField(max_length=255)),
                ('added_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('availability_status', models.CharField(max_length=255)),
                ('added_by', models.CharField(default='block', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateField()),
                ('name', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=255)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bedrooms', models.PositiveIntegerField()),
                ('select_moving_date', models.DateField(default='2023-10-27')),
                ('property_link', models.CharField(default='link', max_length=255)),
                ('lead_source', models.CharField(default='block', max_length=255)),
                ('lead_status', models.CharField(default='block', max_length=255)),
                ('comment', models.CharField(default='block', max_length=10000)),
                ('update', models.CharField(default='No Updates', max_length=255)),
                ('added_by', models.CharField(default='block', max_length=255)),
                ('assigned_to', models.CharField(default='block', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('all_access_on_availability_data', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password_or_otp', models.CharField(max_length=255)),
                ('account_type', models.CharField(default='Account Type', max_length=255)),
                ('last_login_ip', models.GenericIPAddressField()),
                ('new_login_ip_notification', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TenancyContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('close_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('email_notification_sent', models.BooleanField(default=False)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.lead')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_download_link', models.URLField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tenancycontract')),
            ],
        ),
    ]

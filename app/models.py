from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255, default='John')
    email = models.EmailField(default='yaseenuom6@gmail.com')
    phone_no = models.CharField(max_length=20, default='+923029770128')
    password_or_otp = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255, default="Account Type")
    last_login_ip = models.CharField(max_length=255)
    account_status = models.CharField(max_length=255, default="Block")
    new_login_ip_notification = models.CharField(max_length=255, default="False")
    regist_date = models.DateField(default="2023-11-01")

    def __str__(self):
        return self.username


class Availability(models.Model):
    sno = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    community = models.CharField(max_length=255)
    property = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    floor_no = models.PositiveIntegerField()
    unit_no = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    view = models.CharField(max_length=255)
    sqft = models.PositiveIntegerField()
    price = models.BigIntegerField()
    comments = models.CharField(max_length=255)
    added_date = models.DateField()
    status = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    availability_status = models.CharField(max_length=255)
    added_by = models.CharField(max_length=255, default="block")

    def __str__(self):
        return self.owner_name


class Lead(models.Model):
    added_date = models.DateField()
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    select_moving_date = models.DateField(default="2023-10-27")
    property_link = models.CharField(max_length=255, default="link")
    lead_source = models.CharField(max_length=255, default="block")
    lead_status = models.CharField(max_length=255, default="block")
    comment = models.CharField(max_length=10000, default="block")
    update = models.CharField(max_length=255, default="No Updates")
    added_by = models.CharField(max_length=255, default="block")
    assigned_to = models.CharField(max_length=255, default="block")

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    # Add other fields as needed


class Manager(models.Model):
    name = models.CharField(max_length=255)
    all_access_on_availability_data = models.BooleanField(default=False)
    # Add other fields as needed


class TenancyContract(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    close_date = models.DateField()
    expiry_date = models.DateField()
    email_notification_sent = models.BooleanField(default=False)
    # Add other fields as needed


class Invoice(models.Model):
    contract = models.ForeignKey(TenancyContract, on_delete=models.CASCADE)
    pdf_download_link = models.URLField()
    # Add other fields as needed

# Define other models similarly for Availability, Offer Letter, and Tenancy Contact

from django import forms
from .models import User, Lead, Availability


class UserForm(forms.Form):
    class Meta:
        model = User
        fields = "__all__"



class CustomAuthenticationForm(forms.Form):
    username = forms.CharField()
    password_or_otp = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password_or_otp = cleaned_data.get('password_or_otp')

        try:
            user = User.objects.get(username=username)

            # Check if the provided password_or_otp matches the stored value in the database
            if user.password_or_otp != password_or_otp:
                raise forms.ValidationError("Invalid username or password.")

        except User.DoesNotExist:
            raise forms.ValidationError("Invalid username or password.")


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'phone_no', 'password_or_otp', 'account_type', 'last_login_ip', 'account_status', 'new_login_ip_notification', 'regist_date']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'


class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'contact_no', 'email', 'location', 'budget', 'bedrooms', 'select_moving_date', 'property_link', 'lead_source', 'lead_status', 'comment', 'update', 'added_by', 'assigned_to']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = '__all__'


class AvailabilityUpdateForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['location', 'community', 'property', 'property_type', 'floor_no', 'unit_no', 'bedrooms', 'bathrooms', 'view', 'sqft', 'price', 'comments', 'added_date', 'status', 'owner_name', 'contact_no', 'email', 'availability_status']


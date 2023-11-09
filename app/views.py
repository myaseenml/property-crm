from .forms import RegistrationForm, LeadForm, LeadUpdateForm, AvailabilityForm, AvailabilityUpdateForm, UserForm
import socket
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Lead, Availability
from .forms import CustomAuthenticationForm
from django.contrib import messages
from datetime import datetime
from django.http import QueryDict
from app.email_send import send_email, get_unique_identifier, send_whatsapp, send_email_manager
from django.db.models import Q
# from app.create_files import create_invoice

def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        del request.session['account_type']
        messages.info(request, "You have been logged out successfully.")

        # Redirect to a different page after logout (e.g., the login page).
    return render(request, 'src/login-form.html')


def index(request):
    if request.session.has_key('username'):
        closed_count = Lead.objects.filter(lead_status='closed').count()
        open_count = Lead.objects.exclude(lead_status='closed').count()
        sale_count = Availability.objects.filter(availability_status='forSale').count()
        rent_count = Availability.objects.filter(availability_status='forRent').count()
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'closed_count': closed_count,
            'open_count': open_count,
            'sale_count': sale_count,
            'rent_count': rent_count,
            'total_sales': sale_count+rent_count
        }
        return render(request, 'src/Dashboard.html', context)
    else:
        return render(request, 'src/login-form.html')


def login(request):
    return render(request, 'src/login-form.html')

def register_page(request):
    return render(request, 'src/register-form.html')


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_or_otp = form.cleaned_data['password_or_otp']

            try:
                user = User.objects.get(username=username)

                # Check if the provided password_or_otp matches the stored value in the database
                if user.password_or_otp != password_or_otp:
                    raise User.DoesNotExist

                # Check if the current system IP matches the stored IP in the database
                current_ip = get_unique_identifier()

                if request.POST.get('remember') == 'on':
                    user_pk = get_object_or_404(User, pk=user.id)  # Fetch the related Lead object
                    user_pk.new_login_ip_notification = True
                    user_pk.account_status = 'block'
                    user_pk.last_login_ip = current_ip
                    user_pk.save()
                    raise User.DoesNotExist

                print(current_ip)
                if user.last_login_ip != current_ip:
                    print("IP wrong")
                    raise User.DoesNotExist
                print(user.account_status)
                if user.account_status == 'block':
                    messages.warning(request, "Your account is locked!")
                    raise User.DoesNotExist

                # If both checks pass, log the user in
                login(request)
                request.session['username'] = user.username
                request.session['account_type'] = user.account_type
                return redirect('/')

            except User.DoesNotExist:
                # Invalid username, password, or IP
                form.add_error(None, "Invalid username, password, or IP.")

    else:
        form = CustomAuthenticationForm()

    return render(request, 'src/login-form.html', {'form': form})


def submit_lead(request):
    if request.method == 'POST':
        # Create a mutable copy of the request.POST QueryDict
        post_data = QueryDict(mutable=True)
        post_data.update(request.POST)

        # Add the 'added_date' field with the current date
        post_data['added_date'] = datetime.now().strftime('%Y-%m-%d')
        post_data['update'] = "No Updates"
        post_data['added_by'] = request.session['username']

        form = LeadForm(post_data)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

        if form.is_valid():
            messages.success(request, "Lead Added Successfully!")
            user = User.objects.get(username=request.POST.get('assigned_to'))

            # Retrieve the phone number for the specific user
            phone_number = user.phone_no
            send_whatsapp(user.fullname, user.phone_no)

            lead = form.save()  # Save the Lead object
            return redirect('leads')
    else:
        form = LeadForm()

    return render(request, 'src/add-lead-1.html', {'form': form})


def lead_update(request, pk):
    # Retrieve the record based on the ID
    lead = get_object_or_404(Lead, pk=pk)
    assigned_to_values = Lead.objects.values_list('assigned_to', flat=True).distinct()
    print(lead, "test")
    sno = 1
    if request.method == 'POST':
        print("This is post")
        # Create a mutable copy of the request.POST QueryDict
        post_data = request.POST.copy()

        # Add the 'added_date' field with the current date
        post_data['added_date'] = datetime.now().strftime('%Y-%m-%d')
        post_data['added_by'] = request.session.get('username', '')

        print(3)

        # Populate a form with the existing data
        form = LeadUpdateForm(post_data, instance=lead)
        print(4)

        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

        print(request.POST.get('assigned_to'))

        if form.is_valid():
            if request.POST.get('lead_status') == 'closed':
                user = User.objects.get(username=request.POST.get('assigned_to'))

                # Retrieve the phone number for the specific user
                phone_number = user.phone_no
                send_whatsapp(user.fullname, user.phone_no)
            print(5)
            messages.success(request, "Lead Updated Successfully!")
            # Update the data in the form with the new data submitted by the user
            form.save()  # Save the updated data to the database
            return redirect('leads')
    else:
        form = LeadUpdateForm(instance=lead)

    return render(request, 'src/update_lead.html', {'form': form, 'pk': pk, 'assigned_to_values': assigned_to_values,})


# View for deleting a lead
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, 'Lead deleted successfully')
    return redirect('leads')  # Redirect to your leads page


def password_reset(request):
    return render(request, 'src/login-form.html')


def register_view(request):
    if request.method == 'POST':
        print(1)
        post_data = QueryDict(mutable=True)
        post_data.update(request.POST)
        username = request.POST.get('username')

        # Check if a user with the specified username exists
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            messages.warning(request, "Username already exists!")
            return redirect('login')

        post_data['last_login_ip'] = get_unique_identifier()
        post_data['account_status'] = "block"
        post_data['new_login_ip_notification'] = "True"
        post_data['regist_date'] = datetime.now().strftime('%Y-%m-%d')

        form = RegistrationForm(post_data)
        print(2)

        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

        if form.is_valid():
            print(3)
            data = ["Property Square", request.POST.get('fullname'), request.POST.get('username'), request.POST.get('email'), post_data['regist_date'], "https://example.com"]
            send_email("Registration", request.POST.get('email'), data)

            manager_users = User.objects.filter(account_type='Manager')

            # Define the data for the email
            data = [
                request.POST.get('fullname'),
                request.POST.get('username'),
                request.POST.get('email'),
                post_data['regist_date'],
            ]

            # Send an email to each manager user
            for manager_user in manager_users:
                send_email_manager("Registration", manager_user.email, data)


            messages.success(request, "Successfully Registered!")
            form.save()  # Save the user registration data to the database
            return render(request, 'src/login-form.html')
    else:
        print(4)
        form = RegistrationForm()

    return render(request, 'src/login-form.html')


def telecalling(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/telecalling.html', context)
    else:
        return render(request, 'src/login-form.html')


def users(request):
    if request.session.has_key('username'):
        users_data = User.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'users': users_data
        }

        return render(request, 'src/users.html', context)
    else:
        return render(request, 'src/login-form.html')


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        print("This is post")
        # Create a mutable copy of the request.POST QueryDict
        post_data = request.POST.copy()
        prim = RegistrationForm(instance=user)
        post_data['regist_date'] = prim['regist_date'].value()
        # post_data['new_login_ip_notification'] = prim['new_login_ip_notification'].value()

        # Populate a form with the existing data
        form = RegistrationForm(post_data, instance=user)
        print(1)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

        if form.is_valid():
            messages.success(request, "User Updated Successfully!")
            # Update the data in the form with the new data submitted by the user
            form.save()  # Save the updated data to the database
            return redirect('users')
    else:

        form = RegistrationForm(instance=user)

    return render(request, 'src/update_user.html', {'form': form, 'pk': pk, 'type': request.session['account_type']})


# View for deleting a lead
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('users')  # Redirect to your leads page


def assign_lead(request):
    if request.session.has_key('username'):
        leads = Lead.objects.all()  # Fetch all leads from the database
        context = {
            'type': request.session['account_type'],
            'leads': leads
        }
        return render(request, 'src/assign_lead.html', context)
    else:
        return render(request, 'src/login-form.html')


def lead_update_assign(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        updated_rows = Lead.objects.filter(pk=pk).update(assigned_to=request.POST.get('assigned_to'))

        if updated_rows == 1:
            user = User.objects.get(username=request.POST.get('assigned_to'))

            send_whatsapp(user.fullname, user.phone_no)
            messages.success(request, f"Lead Assigned to {request.POST.get('assigned_to')} Successfully!")
            return redirect('assign_lead')
        else:
            messages.error(request, f"Lead Assigned to {request.POST.get('assigned_to')} Failed!")
            print("Lead not found or update failed")

    else:
        form = LeadUpdateForm(instance=lead)
        assigned_to_values = Lead.objects.values_list('assigned_to', flat=True).distinct()

    return render(request, 'src/update_agent_assign.html', {'form': form, 'pk': pk, 'type': request.session['account_type'], 'assigned_to_values': assigned_to_values})


def leads(request):
    if request.session.has_key('username'):
        if request.session['account_type'] == "Agent":
            leads = Lead.objects.filter(assigned_to=request.session['username'])
        elif request.session['account_type'] == "Manager":
            leads = Lead.objects.all()  # Fetch all leads from the database
        else:
            leads = Lead.objects.exclude(lead_status='Closed')
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'leads': leads
        }

        return render(request, 'src/Leads.html', context)
    else:
        return render(request, 'src/login-form.html')


def add_lead(request):
    if request.session.has_key('username'):
        assigned_to_values =  list(User.objects.filter(account_type='Agent').values_list('username', flat=True))
        context = {
            'type': request.session['account_type'],
            'assigned_to_values': assigned_to_values,
            'agent': request.session['username']
        }
        return render(request, 'src/add-lead-1.html', context)
    else:
        return render(request, 'src/login-form.html')


def agent(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/agents.html', context)
    else:
        return render(request, 'src/login-form.html')


def manager(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/manager.html', context)
    else:
        return render(request, 'src/login-form.html')


def sale_availability(request):
    if request.session.has_key('username'):
        availabilities = Availability.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'availabilities': availabilities,
            'unique_snos': list(Availability.objects.values_list('sno', flat=True).distinct().order_by('sno')),
            'unique_locations': list(Availability.objects.values_list('location', flat=True).distinct().order_by('location')),
            'unique_communities': list(Availability.objects.values_list('community', flat=True).distinct().order_by('community')),
            'unique_properties': list(Availability.objects.values_list('property', flat=True).distinct().order_by('property')),
            'unique_property_types': list(Availability.objects.values_list('property_type', flat=True).distinct().order_by('property_type')),
            'unique_unit_nos': list(Availability.objects.values_list('unit_no', flat=True).distinct().order_by('unit_no')),
            'unique_bedrooms': list(Availability.objects.values_list('bedrooms', flat=True).distinct().order_by('bedrooms')),
        }

        return render(request, 'src/avalibilityForSale-Rent.html', context)
    else:
        return render(request, 'src/login-form.html')


def add_availability1(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/add-availibility-1.html', context)
    else:
        return render(request, 'src/login-form.html')


def submit_availability(request):
    print(1)
    if request.method == 'POST':
        # Create a mutable copy of the request.POST QueryDict
        post_data = QueryDict(mutable=True)
        post_data.update(request.POST)

        # Add the 'added_date' field with the current date
        post_data['added_date'] = datetime.now().strftime('%Y-%m-%d')
        post_data['added_by'] = request.session['username']

        largest_sno = Availability.objects.all().order_by('-sno').first()
        if largest_sno is not None:
            largest_sno_value = largest_sno.sno
        else:
            largest_sno_value = 0
        largest_sno_value += 1

        post_data['sno'] = largest_sno_value

        form = AvailabilityForm(post_data)

        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

        if form.is_valid():
            messages.success(request, "Availability Added Successfully!")
            form.save()  # Save the Lead object
            return redirect('sale_availability')
    else:
        form = AvailabilityForm()

    return render(request, 'src/add-availibility-1.html', {'form': form})


def availability_update(request, pk):
    # Retrieve the record based on the ID
    availability = get_object_or_404(Availability, pk=pk)
    print(availability, "test")
    sno = 1
    if request.method == 'POST':
        print("This is post")
        # Create a mutable copy of the request.POST QueryDict
        post_data = request.POST.copy()

        # Add the 'added_date' field with the current date
        post_data['added_date'] = datetime.now().strftime('%Y-%m-%d')
        post_data['added_by'] = request.session.get('username', '')

        # Populate a form with the existing data
        form = AvailabilityUpdateForm(post_data, instance=availability)

        if form.is_valid():
            messages.success(request, "Availability Updated Successfully!")
            # Update the data in the form with the new data submitted by the user
            form.save()  # Save the updated data to the database
            return redirect('sale_availability')
    else:
        form = AvailabilityUpdateForm(instance=availability)
        prim = AvailabilityForm(instance=availability)
        sno = prim['sno'].value()

    return render(request, 'src/update_availability1.html', {'form': form, 'sno:': sno, 'pk': pk, 'type': request.session['account_type']})


# View for deleting a lead
def availability_delete(request, pk):
    availability = get_object_or_404(Availability, pk=pk)
    availability.delete()
    messages.success(request, 'Availability deleted successfully')
    return redirect('sale_availability')  # Redirect to your leads page


def invoice_generation(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/invoice.html', context)
    else:
        return render(request, 'src/login-form.html')


def offer_letter(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            # Add other context data if needed
        }
        return render(request, 'src/offerLetter.html', context)
    else:
        return render(request, 'src/login-form.html')


def for_sale_availability(request):
    if request.session.has_key('username'):
        availabilities = Availability.objects.filter(availability_status='forSale')
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'availabilities': availabilities
        }

        return render(request, 'src/avalibilityForSale-Rent.html', context)
    else:
        return render(request, 'src/login-form.html')


def for_rent_availability(request):
    if request.session.has_key('username'):
        availabilities = Availability.objects.filter(availability_status='forRent')
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'availabilities': availabilities
        }

        return render(request, 'src/avalibilityForSale-Rent.html', context)
    else:
        return render(request, 'src/login-form.html')


def generate_invoice(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        product_names = request.POST.getlist('product_name[]')
        items = request.POST.getlist('items[]')
        amounts = request.POST.getlist('amount[]')

        total_amount = sum([int(amount) for amount in amounts])

        data = []
        for i in range(0, len(product_names)):
            data.append([product_names[i], items[i], amounts[i]])

        now = datetime.now()

        context = {
            'filename': customer_name +"-"+ str(now.strftime("%Y-%m-%d %H-%M-%S")),
            'data': data,
            'loop_range': range(0,len(product_names)),
            'customer_name': customer_name,
            'total_amount': total_amount,
            'invoice_number': '12345',  # Replace with your actual invoice number
            'order_date': str(datetime.now().strftime('%Y-%m-%d')),  # Replace with the actual order date
        }

        return render(request, 'src/invoice.html', context)

    return render(request, 'src/invoice.html')


def availability_filter_page(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        availabilities = Availability.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'availabilities': availabilities,
            'unique_snos': list(Availability.objects.values_list('sno', flat=True).distinct().order_by('sno')),
            'unique_locations': list(
                Availability.objects.values_list('location', flat=True).distinct().order_by('location')),
            'unique_communities': list(
                Availability.objects.values_list('community', flat=True).distinct().order_by('community')),
            'unique_properties': list(
                Availability.objects.values_list('property', flat=True).distinct().order_by('property')),
            'unique_property_types': list(
                Availability.objects.values_list('property_type', flat=True).distinct().order_by('property_type')),
            'unique_unit_nos': list(
                Availability.objects.values_list('unit_no', flat=True).distinct().order_by('unit_no')),
            'unique_bedrooms': list(
                Availability.objects.values_list('bedrooms', flat=True).distinct().order_by('bedrooms')),
        }

        return render(request, 'src/availability_filter.html', context)
    else:
        return render(request, 'src/login-form.html')


def availability_filter(request):
    if request.session.has_key('username'):
        filter_cols = [request.POST.get('location'), request.POST.get('community'), request.POST.get('tower'), request.POST.get('bedrooms'), request.POST.get('propertyType'), request.POST.get('unitNo'), request.POST.get('srNo'), request.POST.get('priceFrom'), request.POST.get('priceTo')]

        availability = Availability.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        if filter_cols[0]:
            availability = availability.filter(Q(location=filter_cols[0]))
        if filter_cols[1]:
            availability = availability.filter(Q(community=filter_cols[1]))
        if filter_cols[2]:
            availability = availability.filter(Q(property=filter_cols[2]))
        if filter_cols[3]:
            availability = availability.filter(Q(bedrooms=filter_cols[3]))
        if filter_cols[4]:
            availability = availability.filter(Q(property_type=filter_cols[4]))
        if filter_cols[5]:
            availability = availability.filter(Q(unit_no=filter_cols[5]))
        if filter_cols[6]:
            availability = availability.filter(Q(sno=filter_cols[6]))
        if filter_cols[7] is not None and filter_cols[8] is not None:
            availability = availability.filter(Q(price__gte=filter_cols[7]) & Q(price__lte=filter_cols[8]))


        context = {
            'type': request.session['account_type'],
            'availabilities': availability
        }

        return render(request, 'src/avalibilityForSale-Rent.html', context)
    else:
        return render(request, 'src/login-form.html')


def leads_filter_page(request):
    if request.session.has_key('username'):
        # If the user is already authenticated, you may want to redirect them to another page.
        leads = Lead.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        context = {
            'type': request.session['account_type'],
            'leads': leads,
            'unique_locations': list(Lead.objects.values_list('location', flat=True).distinct().order_by('location')),
            'unique_lead_sources': list(Lead.objects.values_list('lead_source', flat=True).distinct().order_by('lead_source')),
            'unique_lead_statuses': list(
                Lead.objects.values_list('lead_status', flat=True).distinct().order_by('lead_status')),
            'unique_added_bys': list(
                Lead.objects.values_list('added_by', flat=True).distinct().order_by('added_by')),
            'unique_assigned_tos': list(
                Lead.objects.values_list('assigned_to', flat=True).distinct().order_by('assigned_to')),
            'unique_bedrooms': list(
                Lead.objects.values_list('bedrooms', flat=True).distinct().order_by('bedrooms')),
        }

        return render(request, 'src/leads_filter.html', context)
    else:
        return render(request, 'src/login-form.html')


def leads_filter(request):
    if request.session.has_key('username'):
        filter_cols = [request.POST.get('location'), request.POST.get('leadSource'), request.POST.get('leadStatus'), request.POST.get('addBy'), request.POST.get('agent'), request.POST.get('bedrooms')]

        leads = Lead.objects.all()  # Fetch all leads from the database
        # If the user is already authenticated, you may want to redirect them to another page.
        if filter_cols[0]:
            leads = leads.filter(Q(location=filter_cols[0]))
        if filter_cols[1]:
            leads = leads.filter(Q(lead_source=filter_cols[1]))
        if filter_cols[2]:
            leads = leads.filter(Q(lead_status=filter_cols[2]))
        if filter_cols[3]:
            leads = leads.filter(Q(added_by=filter_cols[3]))
        if filter_cols[4]:
            leads = leads.filter(Q(assigned_to=filter_cols[4]))
        if filter_cols[5]:
            leads = leads.filter(Q(bedrooms=filter_cols[5]))


        context = {
            'type': request.session['account_type'],
            'leads': leads
        }

        return render(request, 'src/Leads.html', context)
    else:
        return render(request, 'src/login-form.html')


def download_letter(request):
    if request.session.has_key('username'):
        # create_invoice(request.POST.get('date'), request.POST.get('fullname'), request.POST.get('unitno'), request.POST.get('area'), request.POST.get('utype'), request.POST.get('annrent'), request.POST.get('sec'), request.POST.get('enfee'))

        return redirect('offer_letter')
    else:
        return render(request, 'src/login-form.html')

from django.urls import path
from django.views.generic import RedirectView

from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=True)),
    path('home', views.index, name='home'),
    path('login/', views.custom_login_view, name='login'),
    path('register/', views.register_page, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    # path('login', views.login, name='login'),
    path('register_view', views.register_view, name='register_view'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('telecalling', views.telecalling, name='telecalling'),
    path('users', views.users, name='users'),
    path('assign_lead', views.assign_lead, name='assign_lead'),
    path('leads', views.leads, name='leads'),
    path('add_lead', views.add_lead, name='add_lead'),
    path('agent', views.agent, name='agent'),
    path('manager', views.manager, name='manager'),
    path('sale_availability', views.sale_availability, name='sale_availability'),
    path('availability_filter_page', views.availability_filter_page, name='availability_filter_page'),
    path('availability_filter', views.availability_filter, name='availability_filter'),
    path('for_sale_availability', views.for_sale_availability, name='for_sale_availability'),
    path('for_rent_availability', views.for_rent_availability, name='for_rent_availability'),
    path('add_availability1', views.add_availability1, name='add_availability1'),
    # path('add_availability2', views.add_availability2, name='add_availability2'),
    path('invoice_generation', views.invoice_generation, name='invoice_generation'),
    path('offer_letter', views.offer_letter, name='offer_letter'),
    path('logout', views.logout, name='logout'),
    path('submit_lead', views.submit_lead, name='submit_lead'),
    path('lead/update/<int:pk>/', views.lead_update, name='lead_update'),
    path('lead/delete/<int:pk>/', views.lead_delete, name='lead_delete'),
    path('submit_availability', views.submit_availability, name='submit_availability'),
    path('availability/update/<int:pk>/', views.availability_update, name='availability_update'),
    path('availability/delete/<int:pk>/', views.availability_delete, name='availability_delete'),
    path('user/update/<int:pk>/', views.user_update, name='user_update'),
    path('user/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('agent/lead/update/<int:pk>/', views.lead_update_assign, name='lead_update_assign'),
    path('generate_invoice/', views.generate_invoice, name='generate_invoice'),
    path('leads_filter_page', views.leads_filter_page, name='leads_filter_page'),
    path('leads_filter', views.leads_filter, name='leads_filter'),
    path('download_letter', views.download_letter, name='download_letter'),
]

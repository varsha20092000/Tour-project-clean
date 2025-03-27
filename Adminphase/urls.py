from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path('adminlogin/', views.Adminlogin_view, name='adminlogin'),
    path('adminhomepage/', views.Adminhomepage, name='adminhomepage'),
    path('traveller_list/', views.traveller_list, name='traveller_list'),
    path('company_list/', views.company_list, name='company_list'),
    path('customized-tour-management/', views.customized_tour_management, name='customized_tour_management'),
    path('addpackage', views.Addpackage, name='Addpackage'),
     path('adminphase/package/update/<uuid:pk>/', views.PackageUpdateView.as_view(), name='update-package'),
    path('adminphase/package/delete/<uuid:pk>/', views.PackageDeleteView.as_view(), name='delete-package'),
    path('customer-info/', views.customer_info, name='customer_info'),
    path('payment_management/', views.payment_management, name='payment_management'),
    path('subscription_list/', views.subscription_list, name='subscription_list'),
    path('add-subscription/', views.add_subscription, name='add_subscription'),
    path('visa-management/', views.visa_management_page, name='visa_management'),
    path('create-role/', views.create_role, name='create_role'),
    path('settings/', views.settings_page, name='settings_page'),
    path('settings/save/', views.save_settings, name='save_settings'),
    path('', views.roles_list, name='roles_list'),
    path('delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('generate-credentials/', views.generate_credentials, name='generate_credentials'),
    path('success/', views.credentials_success, name='credentials_success'),
    path('teammembers/', views.teammember_list, name='teammembers_list'),  # Correct this view name

    # URL for viewing details of an individual member
    path('<str:member_id>/', views.member_detail, name="member_detail"),  # This must come after the above URL

    # URL for team member detail (if you need it)
    path('detail/', views.teammember_detail, name='team_members_detail'),
    
    # This one seems redundant now since you already have <str:member_id>/ pattern
    path('member_list', views.member_list, name="member_list"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.db import models
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class AdminManager(BaseUserManager):
    def create_user(self, admin_id, password=None, **extra_fields):
        if not admin_id:
            raise ValueError('The Admin ID must be set')
        admin = self.model(admin_id=admin_id, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, admin_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(admin_id, password, **extra_fields)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='admin')
    admin_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.admin_id


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'password')
from django.utils import timezone
class Traveller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="Unknown Traveller")  # ✅ Add default name
    package_choice = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Pending', 'Pending')])
    tour_type = models.CharField(max_length=50, choices=[('Solo', 'Solo'), ('Group', 'Group')])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_tour = models.DateField()
    country_code = models.CharField(max_length=10, default="+91")  
    phone = models.CharField(max_length=15, default="Not Provided")  
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from django.db import models


from django.contrib.auth.models import User  # explicitly Django's built-in model

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_companies")
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    country_code = models.CharField(max_length=10, default="+91")
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class TourRequest(models.Model):
    customer_name = models.CharField(max_length=255)
    travel_request_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    requested_datetime = models.DateTimeField()
    package_info = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('Acknowledged', 'Acknowledged'), ('Processing', 'Processing'), ('Complete', 'Complete')])

    def __str__(self):
        return f"{self.customer_name} - {self.travel_request_id}"
    
class AddNewPackage(models.Model):
    PACKAGE_TYPES = [
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    ]

    package_id = models.CharField(max_length=10, unique=True)
    package_type = models.CharField(max_length=15, choices=PACKAGE_TYPES)
    phone_number = models.CharField(max_length=15)
    requested_date_time = models.DateTimeField()
    package_info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.package_id} - {self.package_type}"
import uuid   
class Package(models.Model):
    package_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='package_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return f"Image for {self.package.name}"
class Customer(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    message = models.CharField(max_length=255)
    email = models.EmailField()
    gender_choices = [('Male', 'Male'), ('Female', 'Female')]
    gender = models.CharField(choices=gender_choices, max_length=10)
    admin_response_choices = [('Pending', 'Pending'), ('Responded', 'Responded')]
    admin_response = models.CharField(choices=admin_response_choices, max_length=10)

    def __str__(self):
        return self.name
    
class PaymentManagement(models.Model):
    PAYMENT_TYPES = [
        ('travellers', 'Payment list of Travellers'),
        ('companies', 'Payment list of Companies'),
        ('visa', 'Payment list Visa'),
        ('customized', 'Payment list for Customized Package'),
        ('pre_planned', 'Payment list for Pre-planned Package'),
        ('status', 'Payment Status (Company and Traveller)'),
    ]
    type = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.type

class Subscription(models.Model):
    subscription_id = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    time_duration = models.IntegerField()  # in months
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100)
    any_change = models.BooleanField(default=False)

    def __str__(self):
        return self.subscription_id


class SubscriptionPlan(models.Model):
    subscription_time = models.CharField(max_length=50, choices=[
        ('1 month', '1 month'),
        ('2 months', '2 months'),
        ('6 months', '6 months'),
        ('12 months', '12 months'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=50, choices=[
        ('1 month - Rs.100 OFF', '1 month - Rs.100 OFF'),
        ('4 months - Rs.200 OFF', '4 months - Rs.200 OFF'),
        ('6 months - Rs.300 OFF', '6 months - Rs.300 OFF'),
    ])
    additional_offers = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subscription_time} - Rs.{self.price}"

class VisaRequest(models.Model):
    visa_request_id = models.CharField(max_length=10, unique=True)
    date_and_time = models.DateField()
    visa_requested_country = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=15)
    purpose_for_visa = models.CharField(max_length=50, choices=[("Travel", "Travel")])
    admin_response = models.CharField(
        max_length=100,
        choices=[
            ("Collected information", "Collected information"),
            ("Issued Visa and received payment", "Issued Visa and received payment"),
            ("Completed process", "Completed process"),
        ],
    )

    def __str__(self):
        return self.visa_request_id
    
class  CreateRole(models.Model):
    role_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.role_name
    
class SettingRole(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class AddedRole(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateField()

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    aadhar_card = models.FileField(upload_to='aadhar_cards/')
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    document_verification = models.BooleanField(default=False)
    joining_date = models.DateField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class EmployeeCredential(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=10, unique=True, default="DEFAULT_ID")
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.name
    
class ExtendedTeamMember(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = models.DateField()
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name

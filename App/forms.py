from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Package,Contact


class  RegistrationForm(UserCreationForm): 
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta: 
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})

        }
    
        

class LoginForm(forms.ModelForm): 
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta: 
            model=User
            fields = ['username', 'password'] 
            widgets = { 
        "username":forms.TextInput(attrs={"class":"form-control"}),
        "password":forms.PasswordInput(attrs={"class":"form-control"})
     } 
            def authenticate_user(self): 
                username = self.cleaned_data.get('username') 
                password = self.cleaned_data.get('password') 
                user = authenticate(username=username, password=password) 
                if user is None: 
                    raise forms.ValidationError("Invalid username or password") 
                return user   


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'  # Or specify which fields you need
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    # Additional fields for user info and payment
    name = forms.CharField(max_length=100, label="Full Name")
    age = forms.IntegerField(label="Age")
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')],
        label="Gender"
    )
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")
    aadhaar_number = forms.CharField(max_length=12, label="Aadhaar Card Number")
    
    payment_method = forms.ChoiceField(
        choices=[('net_banking', 'Net Banking'), ('debit_card', 'Debit Card')],
        label="Payment Method"
    )
    net_banking_provider = forms.CharField(required=False, label="Bank Name (if Net Banking)")
    debit_card_provider = forms.CharField(required=False, label="Bank Name (if Debit Card)")
    card_number = forms.CharField(required=False, label="Card Number")
    expiration_date = forms.DateField(required=False, label="Expiration Date (MM/YYYY)")
    cvv = forms.CharField(required=False, label="CVV")

    class Meta:
        model = Booking
        exclude = ['tour', 'user', 'total_price', 'status', 'banking_details']
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
from .models import CompanyProfile

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'name',
            'icon',
            'phone_number',
            'email',
            'location',
            'description',
            'programmes_file',
            'package_details_file'
        ]
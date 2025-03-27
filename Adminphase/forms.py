from django import forms
from .models import SubscriptionPlan


class AdminLoginForm(forms.Form):
    admin_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Admin ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['subscription_time', 'price', 'discount', 'additional_offers']
        widgets = {
            'subscription_time': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'discount': forms.Select(attrs={'class': 'form-control'}),
            'additional_offers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter offers'}),
        }

from .models import CreateRole

class RoleForm(forms.ModelForm):
    class Meta:
        model = CreateRole
        fields = ['role_name', 'phone_number', 'description']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agent'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '91334556710'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
        }

from .models import TeamMember

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

from .models import EmployeeCredential

class EmployeeCredentialForm(forms.ModelForm):
    class Meta:
        model = EmployeeCredential
        fields = ['name', 'role', 'user_id', 'password', 'employee_id']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        }

from .models import Package

class PackageForm(forms.ModelForm):
    additional_images = forms.FileField(
        required=False
    )

    class Meta:
        model = Package
        fields = ['name', 'description', 'destination', 'duration', 'price', 'main_image']

    def save(self, commit=True):
        instance = super(PackageForm, self).save(commit)
        return instance

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import AdminLoginForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Admin
from .models import Company,Package,PackageImage
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Traveller
from App.models import Booking
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PackageForm
from django.urls import reverse_lazy
def is_admin(user):
    return user.is_authenticated and user.is_superuser  # Only allow superusers


def Adminlogin_view(request):
    if request.method == "POST":
        admin_id = request.POST.get('admin-id')
        password = request.POST.get('password')

        user = authenticate(username=admin_id, password=password)

        print(f"DEBUG: Attempting to authenticate admin: {admin_id}")  # ✅ Debugging

        if user is not None:
            if user.is_superuser:  # ✅ Ensure it's an admin
                login(request, user)  # ✅ Log the user in
                request.session['admin_id'] = user.username  # ✅ Store admin session
                request.session['is_admin'] = True  # ✅ Mark as admin session
                request.session.modified = True  # ✅ Force session save
                print(f"DEBUG: Logged in as admin {user.username}, session stored, redirecting to {settings.ADMIN_LOGIN_REDIRECT_URL}") 
                return redirect(settings.ADMIN_LOGIN_REDIRECT_URL)
            else:
                print("DEBUG: User is not an admin")
                return render(request, 'adminlogin.html', {'error': 'Not an admin'})
        else:
            print("DEBUG: Invalid credentials")
            return render(request, 'adminlogin.html', {'error': 'Invalid credentials'})

    return render(request, 'adminlogin.html')
from django.contrib.auth.hashers import check_password

def authenticate_admin(admin_id, password):
    try:
        admin = Admin.objects.get(admin_id=admin_id)
        if check_password(password, admin.password):  # Use hashed password check
            return True
        return False
    except Admin.DoesNotExist:
        return False

@login_required(login_url=settings.ADMIN_LOGIN_URL) 
@user_passes_test(is_admin) # Ensure only logged-in admins can access
def Adminhomepage(request):
    admin_id = request.session.get('admin_id', None)
    print(f"DEBUG: Admin session ID: {admin_id}")  # Debugging

    if not admin_id:
        print("DEBUG: No admin session, redirecting to login")  # Debugging
        return redirect(settings.ADMIN_LOGIN_URL)

    # ✅ Fetch admin user details
    try:
        admin_user = User.objects.get(username=admin_id)
    except User.DoesNotExist:
        print("DEBUG: Admin user not found, logging out")
        return redirect(settings.ADMIN_LOGIN_URL)

    return render(request, 'adminhome.html', {'admin_user': admin_user})
from .models import Traveller
def is_admin(user):
    return user.is_staff or user.is_superuser  # Ensure this function exists

@user_passes_test(is_admin)
def traveller_list(request):
    travellers = Traveller.objects.all()  
    print(f"Travellers: {list(travellers)}")  # Convert to list for debugging
    return render(request, 'traveller_list.html', {'travellers': travellers})
@user_passes_test(is_admin)
def company_list(request):
    companies = Company.objects.all()

    # ✅ Fetch the dynamic counts
    traveller_count = Traveller.objects.count()
    company_count = Company.objects.count()

    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = [session.get_decoded().get('_auth_user_id') for session in sessions if session.get_decoded().get('_auth_user_id')]
    active_now_count = User.objects.filter(id__in=uid_list).distinct().count()

    context = {
        'companies': companies,
        'traveller_count': traveller_count,
        'company_count': company_count,
        'active_now_count': active_now_count,
    }

    return render(request, 'company_list.html', context)
from .models import TourRequest,AddNewPackage

def customized_tour_management(request):
    tours = TourRequest.objects.all()
    return render(request, 'tour_management.html', {'tours': tours})

def Addpackage(request):
    packages = AddNewPackage.objects.all()
    search_query = request.GET.get('search', '')
    filter_query = request.GET.get('filter', '')

    if search_query:
        packages = packages.filter(package_info__icontains=search_query)

    if filter_query == 'Domestic':
        packages = packages.filter(package_type='Domestic')
    elif filter_query == 'International':
        packages = packages.filter(package_type='International')

    context = {
        'packages': packages,
    }
    return render(request, 'Addnewpackage.html', context)
class PackageCreateView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'adminphase/addnewpackage.html'
    success_url = reverse_lazy('package-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('additional_images')
        for image in images:
            PackageImage.objects.create(package=self.object, image=image)
        return response

class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'adminphase/updatepackage.html'
    success_url = reverse_lazy('package-list')

class PackageDeleteView(DeleteView):
    model = Package
    template_name = 'adminphase/deletepackage.html'
    success_url = reverse_lazy('package-list')
def package_list_view(request):
    packages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': packages})

from .models import Customer

def customer_info(request):
    users = User.objects.all()

    user_details = []
    for user in users:
        traveller = Traveller.objects.filter(user=user).first()
        company = Company.objects.filter(user=user).first()

        phone = traveller.phone if traveller else (company.phone if company else "Not Provided")

        user_details.append({
            "id": user.id,
            "username": user.username,
            "date_joined": user.date_joined,
            "email": user.email,
            "phone": phone,
            "is_active": user.is_active
        })

    context = {"users": user_details}
    return render(request, "customer_management.html", context)

from .models import PaymentManagement

def payment_management(request):
    # Fetch all payment types (you can customize filters here)
    payments = PaymentManagement.objects.all()
    return render(request, 'payment_management.html', {'payments': payments})
from .models import Subscription

def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscription-list.html', {
        'subscription_list': subscriptions
    })

from .forms import SubscriptionPlanForm

def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'subscription-list.html')  # Redirect after success
    else:
        form = SubscriptionPlanForm()
    return render(request, 'add_subscription.html', {'form': form})

from .models import VisaRequest

def visa_management_page(request):
    visa_requests = VisaRequest.objects.all()  # Fetch all visa requests
    return render(request, 'visa_management.html', {'visa_requests': visa_requests})

from .forms import RoleForm

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_role')  # Redirect to the same page or another one
    else:
        form = RoleForm()

    return render(request, 'create_role.html', {'form': form})


from django.http import JsonResponse
from .models import SettingRole
from django.shortcuts import render

def settings_page(request):
    roles = SettingRole.objects.all()
    return render(request, 'setting.html', {'roles': roles})

def save_settings(request):
    if request.method == 'POST':
        selected_roles = request.POST.getlist('selected_roles')
        # Logic to handle saving selected roles can go here
        return JsonResponse({'message': 'Settings saved!', 'selected_roles': selected_roles})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from .models import AddedRole
def roles_list(request):
    roles = AddedRole.objects.all()
    return render(request, 'addedroles_list.html', {'roles': roles})

def delete_role(request, role_id):
    try:
        role = AddedRole.objects.get(id=role_id)
        role.delete()
        return JsonResponse({'success': True})
    except AddedRole.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Role not found'})
    

from .models import TeamMember
from .forms import TeamMemberForm

def create_profile(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_profile')  # Redirect to a clean form
    else:
        form = TeamMemberForm()

    return render(request, 'create_profile.html', {'form': form})


from django.forms import modelformset_factory
from .models import EmployeeCredential
from .forms import EmployeeCredentialForm

def generate_credentials(request):
    EmployeeFormSet = modelformset_factory(EmployeeCredential, form=EmployeeCredentialForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = EmployeeFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('credentials_success')
    else:
        formset = EmployeeFormSet(queryset=EmployeeCredential.objects.none())

    return render(request, 'generate_credentials.html', {'formset': formset})

def credentials_success(request):
    return render(request, 'credentials_success.html', {})


from .models import TeamMember
from django.shortcuts import render, get_object_or_404

def member_list(request):
    members = [
        {"name": "George", "member_id": "100011", "avatar": "george.png"},
        {"name": "Maria", "member_id": "100234", "avatar": "maria.png"},
        {"name": "James", "member_id": "100455", "avatar": "james.png"},
        {"name": "Darell", "member_id": "100366", "avatar": "darell.png"},
        {"name": "Mohan", "member_id": "100453", "avatar": "mohan.png"},
    ]
    return render(request, "team_memberslist.html", {"members": members})

def member_detail(request, member_id):
    # Dummy data for testing
    dummy_data = {
        "100011": {
            "name": "George",
            "member_id": "100011",
            "gender": "Male",
            "phone_number": "1234567890",
            "role": "Developer",
            "address": "123 Street, City",
            "avatar": "/static/images/george.png",
        },
        "100234": {
            "name": "Maria",
            "member_id": "100234",
            "gender": "Female",
            "phone_number": "9876543210",
            "role": "Manager",
            "address": "456 Avenue, City",
            "avatar": "/static/images/maria.png",
        },
        "100455": {
            "name": "James",
            "member_id": "100455",
            "gender": "Male",
            "phone_number": "1122334455",
            "role": "Designer",
            "address": "789 Boulevard, City",
            "avatar": "/static/images/james.png",
        },
        "100366": {
            "name": "Darell",
            "member_id": "100366",
            "gender": "Female",
            "phone_number": "5566778899",
            "role": "Tester",
            "address": "101 Highway, City",
            "avatar": "/static/images/darell.png",
        },
        "100453": {
            "name": "Mohan",
            "member_id": "100453",
            "gender": "Male",
            "phone_number": "2233445566",
            "role": "Analyst",
            "address": "202 Expressway, City",
            "avatar": "/static/images/mohan.png",
        },
    }
    member = dummy_data.get(member_id, {})
    return render(request, "team_membersdetail.html", {"member": member})

from django.shortcuts import render
from .models import ExtendedTeamMember

from django.shortcuts import render

def teammember_list(request):
    # List of dummy team members
    team_members = [
        {
            "name": "John Doe",
            "employee_id": "EMP001",
            "phone_number": "123-456-7890",
            "profile_picture": "john_doe.png",  # Filename of the profile picture in the static/images folder
        },
        {
            "name": "Jane Smith",
            "employee_id": "EMP002",
            "phone_number": "234-567-8901",
            "profile_picture": "jane_smith.png",
        },
        {
            "name": "Bob Johnson",
            "employee_id": "EMP003",
            "phone_number": "345-678-9012",
            "profile_picture": "bob_johnson.png",
        },
        {
            "name": "Alice Brown",
            "employee_id": "EMP004",
            "phone_number": "456-789-0123",
            "profile_picture": "alice_brown.png",
        },
        # Add more team members here...
    ]
    
    return render(request, 'memberslist.html', {'members': team_members})

from django.shortcuts import render, get_object_or_404

def teammember_detail(request, employee_id):
    # Replace dummy data with actual database query as needed
    team_members = {
        "EMP001": {
            "name": "John Doe",
            "employee_id": "EMP001",
            "user_id": "USR001",
            "phone_number": "123-456-7890",
            "gender": "Male",
            "dob": "1990-01-01",
            "email": "johndoe@example.com",
            "address": "123 Main St, Springfield",
        },
        "EMP002": {
            "name": "Jane Smith",
            "employee_id": "EMP002",
            "user_id": "USR002",
            "phone_number": "234-567-8901",
            "gender": "Female",
            "dob": "1992-03-05",
            "email": "janesmith@example.com",
            "address": "456 Oak Ave, Metropolis",
        },
        
    }
    
    # Fetch member details
    member = team_members.get(employee_id)
    if not member:
        return render(request, "404.html", {})  # Render a 404 page if member not found
    
    return render(request, "memberdetail.html", {"member": member})





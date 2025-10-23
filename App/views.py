from django.shortcuts import render
from App.forms import RegistrationForm,LoginForm

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from App import forms
from django.core.exceptions import ValidationError
from .models import Destination,Wishlist
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Package
from .models import Booking, Tour
from .forms import BookingForm,ContactForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import Traveller

class WelcomeView(View): 
    def get(self, request, *args, **kwargs): 
        return render(request, 'welcome.html')

import json
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from .models import Traveller

# Function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

@csrf_exempt
def send_registration_otp(request):
    print("✅ send_registration_otp triggered with", request.method)
    """Send OTP to the user's email."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            otp = generate_otp()
            request.session["otp"] = otp
            request.session["otp_email"] = email
            request.session["otp_expiry"] = str(now() + timedelta(minutes=5))  # OTP expires in 5 mins

            # Send OTP via email
            subject = "Your OTP Code"
            message = f"Your OTP code is: {otp}. It expires in 5 minutes."
            from_email = "noreply@yourwebsite.com"
            send_mail(subject, message, from_email, [email], fail_silently=False)

            return JsonResponse({"success": True, "message": "OTP sent successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

@csrf_exempt
def verify_otp(request):
    """Verify the OTP entered by the user."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            entered_otp = data.get("otp")
            session_otp = request.session.get("otp")
            otp_expiry_str = request.session.get("otp_expiry")  # Stored as string

            if not entered_otp:
                return JsonResponse({"success": False, "error": "OTP is required."})

            if not session_otp or not otp_expiry_str:
                return JsonResponse({"success": False, "error": "OTP expired or not found."})

            # ✅ Convert expiry string back to datetime object
            otp_expiry = parse_datetime(otp_expiry_str)

            if otp_expiry and now() > otp_expiry:
                return JsonResponse({"success": False, "error": "OTP has expired. Request a new one."})

            if str(entered_otp) == str(session_otp):
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Invalid OTP. Please try again."})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)



from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.utils import timezone
from App.models import Traveller as AppTraveller
from Adminphase.models import Traveller as AdminTraveller
from django.utils import timezone  # Import for timestamps
from App.models import Company
from App.models import Company as AppCompany  # ✅ Ensure this line is present
from django.contrib.auth.models import User
from django.db import IntegrityError
from Adminphase.models import Traveller as AdminTraveller, Company as AdminCompany
def SignUpView(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        country_code = request.POST.get("country_code", "+91")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        is_traveller = request.POST.get("isTraveller", "false").lower() == "true"
        is_company = request.POST.get("isCompany", "false").lower() == "true"

        print("📌 DEBUG Received Data:", request.POST)
        print(f"🚀 isTraveller: {is_traveller}, 🏢 isCompany: {is_company}")

        if password1 != password2:
            return render(request, "register.html", {"popup_error": "Passwords do not match"})

        # ✅ Check for duplicates before creating user
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"popup_error": "Username already exists. Please choose another."})
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"popup_error": "This email is already registered."})

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=make_password(password1),
            )
            user.save()
            print(f"✅ User Created: {user.username} (ID: {user.id})")
        except IntegrityError as e:
            return render(request, "register.html", {"popup_error": "A registration error occurred. Try again."})

        if is_traveller and is_company:
            return render(request, "register.html", {"popup_error": "Please select only one option."})

        if is_traveller:
            app_traveller = AppTraveller.objects.create(
                name=f"{first_name} {last_name}",
                user=user,
                phone=phone,
                package_choice="None",
                status="Pending",
                tour_type="Solo",
                gender=request.POST.get("gender", "Male"),
                date_of_tour=request.POST.get("date_of_tour", timezone.now().date()),
                country_code=country_code,
            )
            print(f"🎉 AppTraveller Created: {app_traveller}")

            admin_traveller = AdminTraveller.objects.create(
                name=f"{first_name} {last_name}",
                user=user,
                phone=phone,
                package_choice="None",
                status="Pending",
                tour_type="Solo",
                gender=request.POST.get("gender", "Male"),
                date_of_tour=request.POST.get("date_of_tour", timezone.now().date()),
                country_code=country_code,
                created_at=timezone.now(),
            )
            print(f"🎉 AdminTraveller Created: {admin_traveller}")

        elif is_company:
            print("🏢 Creating Company Profile...")
            app_company = AppCompany.objects.create(
                company_name=f"{first_name} {last_name}",
                user=user,
                phone=phone,
                email=email,
                country_code=country_code,
                status="Pending",
                registered_at=timezone.now(),
            )
            print(f"🎉 AppCompany Created: {app_company}")

            admin_company = AdminCompany.objects.create(
                company_name=f"{first_name} {last_name}",
                user=user,
                phone=phone,
                email=email,
                country_code=country_code,
                status="Pending",
                registered_at=timezone.now(),
            )
            print(f"🎉 AdminCompany Created: {admin_company}")

        return redirect("signin")

    return render(request, "register.html")
def logout_view(request):
    logout(request)
    return redirect('signin')  
class SignInView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)

                # Check if this user is a registered company
                if hasattr(user, 'admin_companies') and user.admin_companies.exists():
                    if not request.session.get("subscription_completed"):
                        return redirect('/subscriptions/')
                
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        
        return render(request, 'login.html', {'form': form})
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the parent implementation to get the default context
        context = super().get_context_data(**kwargs)

        # Add custom data to the context
        context['carousel_images'] = [
            {"url": "static/images/destination1.jpg", "alt": "Dream Destination 1"},
            {"url": "static/images/destination2.jpg", "alt": "Dream Destination 2"},
            {"url": "static/images/destination3.jpg", "alt": "Dream Destination 3"},
        ]

        context['packages'] = [
            {
                "image": "static/images/spain.jpg",
                "title": "Spain",
                "price": "$499",
                "description": "A journey to sunny Spain with its beautiful beaches and rich culture.",
            },
            {
                "image": "static/images/italy.jpg",
                "title": "Italy",
                "price": "$699",
                "description": "Explore the history, art, and food of Italy.",
            },
            {
                "image": "static/images/germany.jpg",
                "title": "Germany",
                "price": "$599",
                "description": "Discover the castles and forests of Germany.",
            },
        ]

        context['travel_types'] = [
            {"type": "Explore", "image": "static/images/explore.jpg"},
            {"type": "Adventure", "image": "static/images/adv.jpg"},
            {"type": "Cultural", "image": "static/images/culture.jpg"},
            {"type": "Eco", "image": "static/images/eco.jpg"},
            {"type": "Beach", "image": "static/images/beach.jpg"},
            {"type": "Wildlife", "image": "static/images/wildlife.jpg"},
        ]

        return context
# List all destinations
class DestinationListView(ListView):
    model = Destination
    template_name = 'destination_list.html'  
    context_object_name = 'destinations'  
     
    def get_queryset(self):
       
        return Destination.objects.filter(location__icontains='beach')

# Detail of a single destination
class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destination_detail.html'  
    context_object_name = 'destination'
    
    def get_object(self):
        destination = super().get_object()
        print(f'DestinationDetailView accessed with pk: {self.kwargs["pk"]}')
        return destination
    def search_destination(request):
        query = request.GET.get('q')  # Assuming your search bar sends a 'q' parameter
        destination = Destination.objects.filter(name__icontains=query).first()
        return render(request, 'destination_detail.html', {'destination': destination})

from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        user = self.request.user
        print(f"User: {user}, Authenticated: {user.is_authenticated}")

        return Wishlist.objects.filter(user_id=user.id)  
    # List all packages
class PackageListView(ListView):
    model = Package
    template_name = 'package_list.html'  # Template to display the list
    context_object_name = 'packages'
    paginate_by = 10  # Pagination
    def get_queryset(self):
        return Package.objects.all().order_by('id')  # Or your desired field
    def package_list(request):
        tours = Tour.objects.all()  # Fetch all Tour objects
        return render(request, 'package_list.html', {'tours': tours})

# View a single package in detail
class PackageDetailView(DetailView):
    model = Package
    template_name = 'package_detail.html'  # Template to display package details
    context_object_name = 'package'
    


# Create a new package
class PackageCreateView(CreateView):
    model = Package
    template_name = 'package_form.html'  # Template for the create form
    fields = ['name', 'description', 'destination', 'duration', 'price', 'main_image']  # Fields to be filled by the user
    success_url = reverse_lazy('package-list')  # Redirect after successful creation

# Update an existing package
class PackageUpdateView(UpdateView):
    model = Package
    template_name = 'package_form.html'  # Template for the update form
    fields = ['name', 'description', 'destination', 'duration', 'price', 'main_image']  # Fields to be updated
    success_url = reverse_lazy('package-list')  # Redirect after successful update



class BookingFormView(View):
    template_name = 'booknow.html'

    # Predefined package mapping
    package_data = {
        'Norway': {'name': 'Norway', 'description': 'Explore Norway...', 'price': 2000, 'image': 'images/package1.jpg'},
        'Sweden': {'name': 'Sweden', 'description': 'Visit Sweden...', 'price': 2000, 'image': 'images/package2.jpg'},
        'Iceland': {'name': 'Iceland', 'description': 'Experience Iceland...', 'price': 2000, 'image': 'images/fini.jpeg'},
        'Finland': {'name': 'Finland', 'description': 'Discover Finland...', 'price': 2000, 'image': 'images/germ.jpeg'},
        'Germany': {'name': 'Germany', 'description': 'Travel Germany...', 'price': 2000, 'image': 'images/spain1.jpg'},
        'London': {'name': 'London', 'description': 'Visit London...', 'price': 2000, 'image': 'images/la.jpeg'},
    }

    def get(self, request, package_name):
        package = self.package_data.get(package_name)
        if package:
            return render(request, self.template_name, {'package': package})
        # Fallback to a default package or a friendly message
        return render(request, 'booknow.html', {'message': 'This package is not available.'})

    def post(self, request, package_name):
        package = self.package_data.get(package_name)
        if package:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.package_name = package['name']
                booking.booking_date = form.cleaned_data['booking_date']
                booking.number_of_people = form.cleaned_data['number_of_people']
                booking.total_price = package['price'] * form.cleaned_data['number_of_people']
                booking.save()
                return render(request, 'booking-success.html', {'booking': booking})
        # Fallback for invalid post data
        return render(request, self.template_name, {'package': package, 'form': form})

def package_list_view(request):
    featured_packages = Package.objects.filter(is_featured=True)  # Example filter
    other_packages = Package.objects.exclude(is_featured=True)  # Exclude featured ones

    return render(request, 'package_list.html', {
        'featured_packages': featured_packages,
        'other_packages': other_packages
    })
from .models import Tour

def tour_list(request):
    tours = Tour.objects.all()  # Fetch all tours from the database
    return render(request, 'tour_list.html', {'tours': tours})
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Contact Form Submission from {name}"
        body = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        try:
            # Send to you
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # Optional auto-reply
            send_mail(
                "Thanks for contacting TOUR365",
                f"Hi {name},\n\nWe’ve received your message and will respond shortly.\n\n- TOUR365 Team",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect("contact")

        except Exception as e:
            messages.error(request, f"❌ Email failed to send: {e}")

    return render(request, "contact.html")

def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Redirect to a 'thank you' page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

from django.contrib import messages

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the data (optional, if you have a model for Contact)
        # Contact.objects.create(name=name, email=email, subject=subject, message=message)
        
        # Add a success message
        messages.success(request, "Your message has been successfully submitted!")
        return redirect('contact_thank_you')
    return render(request, 'contact.html')

def contact_thank_you(request):
    return render(request, 'contact_thank_you.html')

from django.http import JsonResponse

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the data (optional)
        # Contact.objects.create(name=name, email=email, subject=subject, message=message)

        return JsonResponse({'success': True, 'message': 'Your message has been successfully submitted!'})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def about(request):
    return render(request, 'about.html')
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
import logging
from django.utils.functional import SimpleLazyObject
from django.utils.functional import lazy
@login_required
def profile_view(request):
    user = request.user  # This is already the authenticated User instance

    # Log user details for debugging
    print(f"User: {user}, Type: {type(user)}")

    try:
        # Directly get the profile without extra checks
        profile = get_object_or_404(Profile, user=user)
        print(f"Profile: {profile}")
    except Exception as e:
        print(f"Error retrieving profile: {e}")
        return render(request, 'profile.html', {'error': str(e)})

    return render(request, 'profile.html', {'profile': profile})

def my_trip(request):
    return render(request, 'mytrip.html')

def book_my_trip(request):
    return render(request, 'book_my_trip.html') 


import json
import random
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.mail import send_mail
from django.conf import settings

def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        email = data.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'}, status=400)

        # Generate a random 4-digit OTP
        otp_code = str(random.randint(1000, 9999))

        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp_code}'
        from_email = settings.DEFAULT_FROM_EMAIL  # Ensure this is set in settings.py
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            # Optionally, store otp_code in the session or database for later verification
            return JsonResponse({'success': True, 'message': 'OTP sent', 'otp': otp_code})
        except Exception as e:
            print("Error sending email:", e)
            return JsonResponse({'success': False, 'message': 'Failed to send OTP'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def generate_4_digit_otp():
    """Generate a 4-digit OTP."""
    return str(random.randint(1000, 9999))

@csrf_exempt  # Use with caution; consider CSRF protection for production
def send_login_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            otp_code = generate_4_digit_otp()  # Generate a 4-digit OTP
            print(f"Generated OTP for {email} (Login): {otp_code}")

            # Send OTP via email (Add actual email sending logic here)

            return JsonResponse({"success": True, "otp": otp_code})  # Remove OTP in production

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.contrib import messages

@login_required
def booking_form(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            tour = package.tour 
            # Optionally, if you want to allow bookings even without a tour,
            # remove or modify the following check:
            if tour is None:
                messages.error(request, "This package is not associated with any tour.")
                return redirect("package-detail", pk=package.id)

            booking.tour = tour
            # Force request.user to be a proper user instance:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            booking.user = User.objects.get(pk=request.user.pk)
            
            booking.total_price = calculate_total_price(package, form.cleaned_data.get('number_of_people', 1))
            booking.status = 'Pending'
            booking.banking_details = "Default Banking Info"
            booking.save()
            return redirect("booking-success", booking_id=booking.id)
        else:
            print(form.errors)
    else:
        form = BookingForm()

    return render(request, "booknow.html", {"form": form, "package": package})
@login_required
def booking_success(request, booking_id):
    """Displays the booking confirmation page."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "booking-success.html", {"booking": booking})


# Dummy helper function (replace with your actual logic)
def calculate_total_price(package, number_of_people):
    # Example: Multiply package price by the number of people
    return package.price * int(number_of_people)

def compuser_view(request):
    # Example data; adjust to match your use case
    user_name = "SPACE CENTRE"
    services_description = "Provide your service description"
    price = "15.00"
    discount_price = "5.00"

    return render(request, "compuser.html", {
        "user_name": user_name,
        "services_description": services_description,
        "price": price,
        "discount_price": discount_price,
    })

def subscription_plans_view(request):
    # Example plan data
    show_popup = request.GET.get("redirected") == "1"
    plans = [
        {
            "price": "[ 7-day free trial  !!!! ]",
            "duration": "7 Days subscription",
            "image": "images/sub_plan1.png",
        },
        {
            "price": "₹200",
            "duration": "15 Days subscription",
            "image": "images/sub_plan1.png",
        },
        {
            "price": "₹500",
            "duration": "1 Month subscription",
            "image": "images/sub_plan1.png",
        },
        {
            "price": "₹1200",
            "duration": "3 Month subscription",
            "image": "images/sub_plan2.png",
        },
        {
            "price": "₹2800",
            "duration": "6 Month subscription",
            "image": "images/sub_plan3.png",
        },
        {
            "price": "₹5500",
            "duration": "12 Month subscription",
            "image": "images/sub_plan4.png",
        },
    ]

    # ✅ Check if user is redirected without selecting a plan
  

    return render(request, "subscription_plans.html", {
        "plans": plans,
        "show_popup": show_popup
    })

def payment_options_view(request):
    return render(request, "payment_options.html")
from django.utils.text import slugify

def book_destination(request, destination_id):
    # Retrieve the destination object or return 404 if not found
    destination = get_object_or_404(Destination, pk=destination_id)
    image_map = {
        "Hong Kong": "hongkong_dest.jpg",
        "France": "france.jpg",
        # Add more mappings as needed
    }

    # Get image filename from the map, fallback to slugified default
    image_filename = image_map.get(destination.name, f"{slugify(destination.name)}.jpg")
    if request.method == "POST":
        
        pass

    # For GET requests, render the booking form with destination details.
    context = {
        'destination': destination,
    }
    return render(request, 'book_destination.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Tour
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour, Booking

def booknow_home(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        if not tour_id:
            return render(request, 'no_tour_selected.html')

        tour = get_object_or_404(Tour, id=tour_id)

        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            booking_date=request.POST.get('booking_date'),
            number_of_people=request.POST.get('number_of_people'),
            total_price=tour.price * int(request.POST.get('number_of_people', 1)),
            status='Pending'
        )
        return redirect('booking-success.html', booking_id=booking.id)

    # GET request → show all available tours
    tours = Tour.objects.all()
    return render(request, 'booking_home.html', {'tours': tours})

from .forms import CompanyProfileForm
from .models import CompanyImage

def company_profile_view(request):
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # 'images' is the name for our multiple images input
        if form.is_valid():
            company = form.save()
            # Save each uploaded image linked to the company
            for image in images:
                CompanyImage.objects.create(company=company, image=image)
            # Redirect to a success page or another view (adjust URL name as needed)
            return redirect('subscription_plans')
    else:
        form = CompanyProfileForm()
    return render(request, 'company_profile.html', {'form': form})

def activate_subscription(request):
    request.session['subscription_active'] = True
    return redirect('home')
from .models import Blog
from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, "blog.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    return render(request, "blog_detail.html", {"post": post})

from django.shortcuts import render
from .models import FAQ

def faq_view(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'faq_page.html', {'faqs': faqs})

from django.shortcuts import render

from django.templatetags.static import static

def help_center(request):
    context = {
        'help_img': static('images/help.avif'),  # Use the static helper to get URL
    }
    return render(request, 'help_center.html', context)
# views.py
from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'policy.html')

from django.shortcuts import render

def travel_type_view(request, type_name):
    # Normalize URL param
    type_name = type_name.strip().lower()

    travel_types = {
        "adventure": {
            "name": "Adventure Travel",
            "description": "Adventure travel is about exploring exciting destinations, embracing challenges, and making unforgettable memories along the way.",
            "images": [
                "https://www.lux-reviews.com/wp-content/uploads/2023/10/luxury-adventure-tours-1171x656.jpg",
                "https://cdn.projectexpedition.com/photos/49265touractivityjungleandriveratvadventureprivatefromsanjose3_sized.jpg",
                "https://adm.dookinternational.com/dook/images/experience/uz3tR1619416313.jpg",
                "https://tse2.mm.bing.net/th/id/OIP.sV8tSQNicHt7QJGmcnX8nAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3",
                "https://images.unsplash.com/photo-1528543606781-2f6e6857f318?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YWR2ZW50dXJlJTIwdHJhdmVsfGVufDB8fDB8fHww",
                "https://images.unsplash.com/photo-1707584145698-7a0b425a79e1?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YWR2ZW50dXJlJTIwdHJhdmVsfGVufDB8fDB8fHww",
            ]
        },
        "cultural": {
            "name": "Cultural Travel",
            "description": "Cultural travel lets you dive into history, traditions, and authentic local experiences.",
            "images": [
                "https://wallpapercave.com/wp/wp10918600.jpg",
                "https://touristjourney.com/wp-content/uploads/2020/11/Witness-a-Kathakali-dance-performance-in-our-3-Day-Wildlife-and-culture-tour-of-Thekkady-from-Kochi-1024x684.jpg",
                "https://tse2.mm.bing.net/th/id/OIP.xD3HMcNl5yklGeQfslWLeAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3",
                "https://th.bing.com/th/id/R.ff93393bcbb6cc3c3c0bdef97d673acf?rik=U3Ypn1vC8sdW4g&riu=http%3a%2f%2fwww.springrainadventure.com%2fassets%2fTemplate%2fimages%2fpackages%2ftibet%2fTibet-Cultural-Tour%2fTibet_Cultural-Tours.jpg&ehk=jz%2b6T48oyQNfaEjvw9hzVfsxQcdWqo3U8kCKwMFjn7A%3d&risl=&pid=ImgRaw&r=0",
                "https://tse1.mm.bing.net/th/id/OIP.-HtdyhimXr5Lqy11oNMAfgHaE9?rs=1&pid=ImgDetMain&o=7&rm=3",
                "https://www.indusdiscoveries.com/images/category/banner/1584440392b20200317.jpg",
                "https://blog.thomascook.in/wp-content/uploads/2015/09/Picture118.jpg"
            ]
        },
        "eco": {
            "name": "Eco Travel",
            "description": "Eco travel focuses on sustainable tourism, preserving nature, and supporting local communities.",
            "images": [
                "https://www.thetravelteam.com/wp-content/uploads/2019/01/ecotourism.jpg",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                "https://tse1.mm.bing.net/th/id/OIP.utYlcvJZqy9LwEiVuL833wHaFj?rs=1&pid=ImgDetMain&o=7&rm=3",
                "https://res.cloudinary.com/worldpackers/image/upload/c_limit,f_auto,q_auto,w_1140/wwpxvfamijbpgi5gtbrv",
                "https://th.bing.com/th/id/OIP.QAnffuBeswvXcNmr-iqAxwHaEK?w=326&h=183&c=7&r=0&o=5&dpr=1.6&pid=1.7",
                "https://th.bing.com/th/id/OIP.pb9EoWhQn-aMV6-M-IbbjgHaEO?w=302&h=180&c=7&r=0&o=5&dpr=1.6&pid=1.7"
            ]
        },
        "nature": {
            "name": "Nature Travel",
            "description": "Nature travel is all about connecting with landscapes, wildlife, and the great outdoors.",
            "images": [
                "https://www.adventuretravelcoach.com/wp-content/uploads/2020/06/68AFCE60-6D7A-40C0-BD33-497926A30147.jpeg",
                "https://images.unsplash.com/photo-1501785888041-af3ef285b470"
            ]
        },
        "wildlife": {
            "name": "Wildlife Travel",
            "description": "Wildlife travel brings you close to animals in their natural habitat while promoting conservation.",
            "images": [
                "https://cdn.tourradar.com/s3/content-pages/447/1536x1230/hWPDF2.jpeg",
                "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
                "https://cdn.tourradar.com/s3/tour/original/139221_b9a8e264.jpg",
                "https://th.bing.com/th/id/OADD2.8452611030250_1Y59KZ4SLXVUGFM275?pid=21.2&c=16&roil=0&roit=0&roir=1&roib=1&w=206&dpr=1.6&o=7&rm=3",
                "https://th.bing.com/th/id/OIP.bgmzJwSqrUBNn9hc631dUAHaFj?w=226&h=180&c=7&r=0&o=7&dpr=1.6&pid=1.7&rm=3",
                "https://th.bing.com/th/id/OIP.vQ7VNW-b8LI5CrOhJ9V5_gHaED?w=324&h=180&c=7&r=0&o=7&dpr=1.6&pid=1.7&rm=3"
            ]
        },
        "beach": {
            "name": "Beach Travel",
            "description": "Beach travel is all about sun, sand, and sea — the perfect way to relax or enjoy water adventures.",
            "images": [
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
                "https://images.unsplash.com/photo-1493558103817-58b2924bce98",
                "https://cdn.adventure-life.com/81/11/3/3xenzkcc/1300x820.webp",
                "https://th.bing.com/th/id/OIP.i_69XnPrGMxEqkyWIstWiAHaEw?w=241&h=180&c=7&r=0&o=7&dpr=1.6&pid=1.7&rm=3",
                "https://th.bing.com/th/id/OIP.m9KdaHOWTTveR2hwCGOhEAHaFL?w=258&h=180&c=7&r=0&o=7&dpr=1.6&pid=1.7&rm=3",
                "https://th.bing.com/th/id/OIP.OxZjm5-znolfRoqoGKj_8QHaE8?w=257&h=180&c=7&r=0&o=7&dpr=1.6&pid=1.7&rm=3"
            ]
        },
        "explore": {
            "name": "Exploration Travel",
            "description": "Exploration travel is about discovering hidden gems, remote landscapes, and untouched cultures.",
            "images": [
                "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
                "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800",
                "https://images.unsplash.com/photo-1469474968028-56623f02e42e"
            ]
        }
    }

    # Pick selected travel type or default to adventure
    selected_type = travel_types.get(type_name, travel_types["adventure"])

    return render(request, "travel_type_detail.html", {
        "travel_type": selected_type,
        "images": selected_type["images"]
    })
def travel_detail_view(request, country_name):
    packages = {
        'canada': {
            'title': 'Canada',
            'description': 'Explore the charm of Ottawa with guided city tours and beautiful landscapes.',
            'image': 'images/package1.jpg'
        },
        'finland': {
            'title': 'Finland',
            'description': 'Discover Finland’s serene lakes and the beauty of the Southside region.',
            'image': 'images/package2.jpg'
        },
        'sweden': {
            'title': 'Sweden',
            'description': 'Enjoy the peaceful countryside and historic charm of Jönköping.',
            'image': 'images/package3.jpg'
        },
        'england': {
            'title': 'England',
            'description': 'Visit iconic landmarks and explore London’s vibrant culture.',
            'image': 'images/package4.jpg'
        },
        'iceland': {
            'title': 'Iceland',
            'description': 'Witness Iceland’s stunning volcanic landscapes and geothermal wonders.',
            'image': 'images/package5.jpg'
        },
        'norway': {
            'title': 'Norway',
            'description': 'Explore the scenic fjords and rich history of Oslo.',
            'image': 'images/package6.jpg'
        },
    }

    package = packages.get(country_name.lower())
    if not package:
        return render(request, '404.html', status=404)

    return render(request, 'travel_detail.html', {'package': package})


def travel_section_detail_view(request, section_name):
    sections = {
        'beach': {
            'title': 'Beach Paradise',
            'description': 'Relax on golden sands, swim in crystal clear waters, and enjoy beachside sunsets.',
            'image': 'images/beach.jpg'
        },
        'explore': {
            'title': 'Adventure & Explore',
            'description': 'Embark on thrilling adventures and explore breathtaking natural wonders.',
            'image': 'images/explore.jpg'
        },
        'mountain': {
            'title': 'Mountain Escape',
            'description': 'Breathe fresh air, hike scenic trails, and enjoy panoramic views from mountain peaks.',
            'image': 'images/mountain.jpg'
        },
    }

    section = sections.get(section_name.lower())
    if not section:
        return render(request, '404.html', status=404)

    return render(request, 'travel_section_detail.html', {'section': section})

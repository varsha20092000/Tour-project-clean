from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
# models.py


class CustomUser(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
   
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True) 
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True) 
    bio = models.TextField(blank=True) 
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True) 
    country = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=100, blank=True) 
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self): 
        return self.user.username

from django.db import models

from django.contrib.auth.models import User

class Traveller(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travellers', null=True)
  # ✅ Fix here
    package_choice = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Pending', 'Pending')])
    tour_type = models.CharField(max_length=50, choices=[('Solo', 'Solo'), ('Group', 'Group')])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_tour = models.DateField()
    country_code = models.CharField(max_length=10, default="+91")
    phone = models.CharField(max_length=15, default="Not Provided") 

    def __str__(self):
        return self.name




class Destination(models.Model): 
    name = models.CharField(max_length=100,unique=True) 
    description = models.TextField() 
    location = models.CharField(max_length=255) 
    image = models.ImageField(upload_to='images', blank=True, null=True) 
    best_time_to_visit = models.CharField(max_length=100, blank=True)  
    
    def __str__(self): 
        return self.name

class Tour(models.Model): 
    title = models.CharField(max_length=200) 
    description = models.TextField() 
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours') 
    duration = models.IntegerField(help_text='Duration in days') 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    image = models.ImageField(upload_to='tour_images', blank=True, null=True)
    def __str__(self): 
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.tour.title}'
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating by {self.user.username} for {self.tour.title}'
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tour.title} in wishlist of {self.user.username}'
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_people = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    banking_details = models.TextField(blank=True, null=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE,null=True, blank=True)



    def __str__(self):
        return f'Booking by {self.user.username} for {self.tour.title}'
    class Meta:
        ordering = ['-booking_date']  # Most recent bookings first

    
    
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('Bank Transfer', 'Bank Transfer')])
    status = models.CharField(max_length=20, choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Failed', 'Failed')])

    def __str__(self):
        return f'Payment for {self.booking}'
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)

    def __str__(self):
        return self.title
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'
class Gallery(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Gallery image for {self.tour.title}'
class TourGuide(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    tours = models.ManyToManyField(Tour, related_name='guides')
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
class Package(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Package name
    description = models.TextField()  # Detailed description of the package
    destination = models.ForeignKey(
        Destination, 
        on_delete=models.CASCADE, 
        related_name='packages'
    )  # Related destination
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Package price
    images = models.ImageField(upload_to='images/', blank=True, null=True)  # Main image for the package
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for package creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for package updates

    class Meta:
        ordering = ['id']  # Example: Ordering by `id`, change to your preference


    def __str__(self):
        return self.name
# models.py
from django.db import models

class CompanyProfile(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='company/icons/')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    programmes_file = models.FileField(upload_to='company/programmes/', blank=True, null=True)
    package_details_file = models.FileField(upload_to='company/packages/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class CompanyImage(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/images/')
    
    def __str__(self):
        return f"Image for {self.company.name}"

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="app_companies")
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    country_code = models.CharField(max_length=10, default="+91")
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])
    registered_at = models.DateTimeField(auto_now_add=True)
    has_subscription = models.BooleanField(default=False) 

    def __str__(self):
        return self.company_name

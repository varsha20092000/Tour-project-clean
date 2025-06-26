from django.urls import path
from .views import SignInView,SignUpView,WelcomeView,HomePageView,DestinationDetailView,DestinationListView,WishlistView,PackageCreateView,PackageDetailView,PackageListView,PackageUpdateView,BookingFormView,logout_view
from App import views
from django.conf import settings 
from django.conf.urls.static import static
from .views import send_otp
from django.views.generic import RedirectView
urlpatterns = [
    path('', RedirectView.as_view(url='/signin/', permanent=False)),
    path('welcome/',views. WelcomeView.as_view(), name='welcome'),
    path('signup/',views.SignUpView, name="signup"),
    path('signin/',views.SignInView.as_view(), name='signin'),
    path('home/',views.HomePageView.as_view(),name='home'),
    path('destinations/', views.DestinationListView.as_view(), name='destination_list'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'), 
    path('packages/', views.PackageListView.as_view(), name='package-list'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='package-detail'),
    path('packages/book/<str:package_name>/', views.BookingFormView.as_view(), name='booking_form'),
    path('tours/', views.tour_list, name='tour_list'),
    path('packages/new/', views.PackageCreateView.as_view(), name='package-create'),
    path('packages/<int:pk>/edit/', views.PackageUpdateView.as_view(), name='package-update'),
    path('contact/', views.contact, name='contact'),
    path('contact/thank-you/', views.contact_thank_you, name='contact_thank_you'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('my-trip/', views.my_trip, name='my_trip'),
    path('book-my-trip/', views.book_my_trip, name='book_my_trip'),
    path("booknow/<int:package_id>/",views.booking_form, name='booknow'),
    path("booking-success/<int:booking_id>/", views.booking_success, name="booking-success"),
    path('compuser/',views.compuser_view, name='compuser_profile'),
    path('subscriptions/', views.subscription_plans_view, name='subscription_plans'),
    path('company-profile/', views.company_profile_view, name='company_profile'),
    path('payment-options/', views.payment_options_view, name='payment_options'),
    path('book-destination/<int:destination_id>/', views.book_destination, name='book_destination'),
    path('booknow-home/', views.booknow_home, name='booknow_home'),
    path("send-login-otp/", views.send_login_otp, name="send_login_otp"),
    path("send-registration-otp/", views.send_registration_otp, name="send_registration_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

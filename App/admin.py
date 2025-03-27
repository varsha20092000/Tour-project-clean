
# Register your models here.
from django.contrib import admin
from .models import Destination, Package
from django.contrib import admin
from .models import Destination, Package

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description')
    search_fields = ('name', 'location')

admin.site.register(Destination, DestinationAdmin)
admin.site.register(Package)
from .models import Traveller  # Import your model



from .models import Traveller  # Ensure correct import
@admin.register(Traveller)
class TravellerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'package_choice', 'status', 'tour_type', 'gender', 'date_of_tour')  # ✅ Fixed
    search_fields = ('user_id', 'package_choice', 'tour_type', 'gender')  # ✅ Fixed
    list_filter = ('status', 'tour_type', 'gender')
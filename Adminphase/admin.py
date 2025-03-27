from django.contrib import admin
from django.contrib.auth.models import User

from .models import TeamMember

# Check if the model is not already registered
if not admin.site.is_registered(TeamMember):
    admin.site.register(TeamMember)
from django.contrib.sessions.models import Session
from django.utils.timezone import now

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'expire_date')

    def user(self, obj):
        """Get the user associated with a session"""
        data = obj.get_decoded()
        user_id = data.get('_auth_user_id')
        return User.objects.get(id=user_id) if user_id else None

    def active_sessions(self, request):
        """Return all active sessions"""
        return Session.objects.filter(expire_date__gte=now())

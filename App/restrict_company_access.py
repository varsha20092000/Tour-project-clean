from django.shortcuts import redirect
from django.urls import resolve

class RestrictCompanyWithoutSubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_paths = [
            'subscription_plans',
            'activate_subscription',
            'company_profile',
            'logout',
            'admin:index'
        ]

        current_view = resolve(request.path_info).url_name
        user = request.user

        is_company = request.session.get('is_company')
        has_subscription = request.session.get('subscription_active')

        if (
            user.is_authenticated and 
            is_company and 
            not has_subscription and 
            current_view not in exempt_paths
        ):
            return redirect('/subscriptions/?redirected=1')

        return self.get_response(request)

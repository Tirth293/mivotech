# website/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

class CSRFRefreshMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Ensure CSRF token is set in cookie for all responses
        if hasattr(request, 'META') and request.META.get('CSRF_COOKIE_USED', False):
            get_token(request)
        return response
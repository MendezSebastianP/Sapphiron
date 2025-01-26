import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now, make_aware

class InactivityLogoutMiddleware:
    """
    Middleware to log out users who have been inactive for a specified duration.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            if last_activity:
                # Convert 'last_activity' to timezone-aware datetime
                last_activity_time = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
                last_activity_time = make_aware(last_activity_time)

                # Calculate the elapsed time since last activity
                elapsed_time = now() - last_activity_time

                # If more than 1 hour has passed since last activity, log the user out
                if elapsed_time > datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)

            # Update the 'last_activity' timestamp with the current time
            request.session['last_activity'] = now().strftime('%Y-%m-%d %H:%M:%S')
        
        response = self.get_response(request)
        return response

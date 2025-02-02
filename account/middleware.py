from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            if stored_session_key and stored_session_key != request.session.session_key:
               session_key = Session.objects.filter(session_key=stored_session_key)
               if session_key is not None and len(session_key) > 0:
                   session_key[0].delete()
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()
        response = self.get_response(request)

        return response
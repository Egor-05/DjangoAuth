from django.utils.deprecation import MiddlewareMixin
from .models import Session
from datetime import datetime, timezone
from django.core.exceptions import ObjectDoesNotExist


class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)


class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            return None

        session_id = request.COOKIES.get("session_id")
        if not session_id:
            return None

        try:
            session = Session.objects.get(
                session_id=session_id,
            )
            if (
                session.expires_at < datetime.now(timezone.utc)
                or not session.user.is_active
            ):
                session.delete()
                return
            request.user = session.user
        except ObjectDoesNotExist:
            return

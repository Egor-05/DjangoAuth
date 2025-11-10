from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from jsonschema import validate, ValidationError
from secrets import token_urlsafe

from .models import User, Session
from datetime import datetime, timedelta
import json


class RegisterView(APIView):
    permission_classes = [AllowAny]

    schema = {
        "type": "object",
        "properties": {
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string"},
            "repeat_password": {"type": "string"},
        },
        "required": ["first_name", "last_name", "email", "password", "repeat_password"],
    }

    def post(self, request):
        try:
            validate(instance=json.loads(request.body), schema=self.schema)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        first_name = json.loads(request.body).get("first_name")
        last_name = json.loads(request.body).get("last_name")
        email = json.loads(request.body).get("email")
        password = json.loads(request.body).get("password")
        repeat_password = json.loads(request.body).get("repeat_password")

        if password != repeat_password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email, is_active=True).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, password=password
        )

        session_id = token_urlsafe(32)

        Session.objects.create(
            user=user,
            session_id=session_id,
            expires_at=datetime.now() + timedelta(days=1),
        )

        response = Response(status=status.HTTP_200_OK)

        response.set_cookie("session_id", session_id)
        return response


class AuthView(APIView):
    permission_classes = [AllowAny]

    schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string"},
        },
        "required": ["email", "password"],
    }

    def post(self, request):
        email = json.loads(request.body).get("email")
        password = json.loads(request.body).get("password")

        user = User.objects.filter(email=email, is_active=True).first()
        if not user or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        session_id = token_urlsafe(32)

        Session.objects.create(
            user=user,
            session_id=session_id,
            expires_at=datetime.now() + timedelta(days=1),
        )

        response = Response(status=status.HTTP_200_OK)

        response.set_cookie("session_id", session_id)
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if hasattr(request, "user") and request.user:
            Session.objects.filter(user=request.user).delete()

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("session_id")
        return response


class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response(status=status.HTTP_200_OK)

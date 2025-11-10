from rest_framework.permissions import BasePermission
import json
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import User

from .models import Product


class IsCreatorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        product_name = view.kwargs.get("product_name")
        try:
            creator = Product.objects.get(name=product_name).creator
            print(creator.email)
        except ObjectDoesNotExist:
            return False

        return bool(
            request.user
            and isinstance(request.user, User)
            and request.user.email == creator.email
            or request.user
            and request.user.is_staff
        )


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and isinstance(request.user, User))

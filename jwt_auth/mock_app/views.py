from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsUser, IsCreatorOrAdmin
from rest_framework.permissions import IsAdminUser
from jsonschema import validate, ValidationError
from .serializers import ProductListSerializer
import json


from .models import Product
from authentication.models import User


class CreateProductView(APIView):
    permission_classes = [IsUser]

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "amount": {"type": "integer"},
        },
        "required": ["name", "description", "amount"],
    }

    def post(self, request):
        try:
            validate(instance=json.loads(request.body), schema=self.schema)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        name = json.loads(request.body).get("name")
        description = json.loads(request.body).get("description")
        amount = json.loads(request.body).get("amount")

        if Product.objects.filter(name=name).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Product.objects.create(
            name=name, creator=request.user, description=description, amount=amount
        )

        return Response(status=status.HTTP_201_CREATED)


class PatchDeleteProductView(APIView):
    permission_classes = [IsCreatorOrAdmin]

    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "amount": {"type": "integer"},
        },
        "required": ["description", "amount"],
    }

    def patch(self, request, product_name):
        try:
            validate(instance=json.loads(request.body), schema=self.schema)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        description = json.loads(request.body).get("description")
        amount = json.loads(request.body).get("amount")

        try:
            obj = Product.objects.get(name=product_name)
            obj.description = description
            obj.amount = amount
            obj.save()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, product_name):
        try:
            obj = Product.objects.get(name=product_name)
            obj.delete()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class ShowProductsView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        products = Product.objects.filter(creator__email=request.user.email)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

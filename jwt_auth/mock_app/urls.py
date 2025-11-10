from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateProductView.as_view()),
    path("my/", views.ShowProductsView.as_view()),
    path("<str:product_name>/", views.PatchDeleteProductView.as_view()),
]

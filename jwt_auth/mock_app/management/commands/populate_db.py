from django.core.management.base import BaseCommand
from mock_app.models import Product
from authentication.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = self.create_user('user1@example.com', 'password123')
        user2 = self.create_user('user2@example.com', 'password123')
        admin = self.create_admin_user()

        products = [
            self.create_product('Яблоки', 'Фрукты', 100, user1),
            self.create_product('Хлеб', 'Выпечка', 50, user2),
            self.create_product('Молоко', 'Молочка', 30, user1),
            self.create_product('Сыр', 'Молочка', 20, user2),
            self.create_product('Масло', 'Бакалея', 15, admin),
        ]


    def create_user(self, email, password):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'first_name': 'User', 'last_name': 'Test'}
        )
        if created:
            user.set_password(password)
            user.save()
        return user

    def create_admin_user(self):
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        return admin

    def create_product(self, name, description, amount, creator):
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'creator': creator,
                'amount': amount,
            }
        )
        return product
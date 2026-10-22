from datetime import datetime, timezone as dt_timezone

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from restaurant.models import Booking, Menu


class Command(BaseCommand):
    help = 'Seeds sample menu items, bookings, and demo accounts for Little Lemon.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Little Lemon demo data...')

        # Demo Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@littlelemon.com',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin_user.set_password('LemonAdmin2026!')
        admin_user.save()
        token_admin, _ = Token.objects.get_or_create(user=admin_user)

        customer_user, _ = User.objects.get_or_create(
            username='customer',
            defaults={'email': 'customer@example.com'},
        )
        customer_user.set_password('LemonCustomer2026!')
        customer_user.save()
        token_customer, _ = Token.objects.get_or_create(user=customer_user)

        # Menu Items
        menu_items = [
            {
                'title': 'Greek Salad',
                'price': 12.00,
                'inventory': 25,
                'description': 'Crispy lettuce, peppers, olives and Chicago feta cheese, garnished with garlic croutons.',
            },
            {
                'title': 'Bruschetta',
                'price': 10.00,
                'inventory': 30,
                'description': 'Grilled sourdough bread rubbed with garlic and seasoned with extra-virgin olive oil and salt.',
            },
            {
                'title': 'Grilled Fish',
                'price': 20.00,
                'inventory': 15,
                'description': 'Catch of the day seasoned with lemon butter sauce and Mediterranean herbs.',
            },
            {
                'title': 'Lemon Dessert',
                'price': 8.50,
                'inventory': 20,
                'description': 'Traditional citrus tart served with fresh cream and powdered sugar.',
            },
            {
                'title': 'Pasta',
                'price': 15.00,
                'inventory': 20,
                'description': 'Handcrafted pasta tossed in roasted tomato and basil reduction.',
            },
        ]

        for item_data in menu_items:
            Menu.objects.update_or_create(
                title=item_data['title'],
                defaults=item_data,
            )

        # Bookings
        sample_bookings = [
            {
                'name': 'Adrian',
                'no_of_guests': 4,
                'booking_date': datetime(2026, 11, 1, 19, 0, tzinfo=dt_timezone.utc),
            },
            {
                'name': 'Mario',
                'no_of_guests': 2,
                'booking_date': datetime(2026, 11, 2, 20, 0, tzinfo=dt_timezone.utc),
            },
            {
                'name': 'Jane Doe',
                'no_of_guests': 3,
                'booking_date': datetime(2026, 11, 3, 18, 0, tzinfo=dt_timezone.utc),
            },
        ]

        for b_data in sample_bookings:
            Booking.objects.update_or_create(
                name=b_data['name'],
                booking_date=b_data['booking_date'],
                defaults={'no_of_guests': b_data['no_of_guests']},
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded sample menu items, bookings, and demo accounts!')
        )
        self.stdout.write(f'Admin token: {token_admin.key}')
        self.stdout.write(f'Customer token: {token_customer.key}')

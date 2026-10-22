import json
from datetime import datetime, timezone as dt_timezone

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer


class MenuItemTest(TestCase):
    """
    Unit test for the Menu (MenuItem) model representation and fields.
    Satisfies Coursera Capstone requirement: test_get_item asserting 'IceCream : 80'.
    """

    def test_get_item(self):
        item = Menu.objects.create(title='IceCream', price=80, inventory=100)
        self.assertEqual(str(item), 'IceCream : 80')

    def test_menu_item_fields(self):
        item = Menu.objects.create(
            title='Bruschetta',
            price=10.50,
            inventory=25,
            description='Toasted bread topped with diced tomatoes.',
        )
        self.assertEqual(item.title, 'Bruschetta')
        self.assertEqual(item.name, 'Bruschetta')
        self.assertEqual(float(item.price), 10.50)
        self.assertEqual(item.inventory, 25)
        self.assertEqual(item.menu_item_description, 'Toasted bread topped with diced tomatoes.')


class MenuViewTest(TestCase):
    """
    Unit test for the MenuItemsView API endpoint.
    Tests retrieving all items and token-secured write access.
    """

    def setUp(self):
        self.client = APIClient()
        self.item1 = Menu.objects.create(title='IceCream', price=80, inventory=100)
        self.item2 = Menu.objects.create(title='Pizza', price=120, inventory=50)
        self.user = User.objects.create_user(
            username='chef_mario',
            password='SecretPassword123!',
        )
        self.token = Token.objects.create(user=self.user)

    def test_getall(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_getall_restaurant_path(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_item(self):
        response = self.client.get(f'/api/menu-items/{self.item1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'IceCream')

    def test_post_menu_item_unauthenticated_fails(self):
        payload = {'title': 'Lemon Dessert', 'price': 8.50, 'inventory': 20}
        response = self.client.post('/api/menu-items/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_menu_item_authenticated_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        payload = {'title': 'Lemon Dessert', 'price': '8.50', 'inventory': 20}
        response = self.client.post('/api/menu-items/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.filter(title='Lemon Dessert').count(), 1)


class BookingModelTest(TestCase):
    """
    Unit tests for the Booking model.
    """

    def test_booking_creation_and_string_representation(self):
        now = timezone.now()
        booking = Booking.objects.create(
            name='Adrian',
            no_of_guests=4,
            booking_date=now,
        )
        self.assertEqual(booking.name, 'Adrian')
        self.assertEqual(booking.no_of_guests, 4)
        self.assertEqual(booking.first_name, 'Adrian')
        self.assertEqual(str(booking), f'Adrian : {str(now)}')


class BookingApiTest(TestCase):
    """
    Unit tests for the table booking API endpoint.
    Verifies authentication security (token requirement) and CRUD functionality.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='customer_jane',
            password='JanePassword123!',
        )
        self.token = Token.objects.create(user=self.user)
        self.booking_time = datetime(2026, 11, 15, 18, 0, tzinfo=dt_timezone.utc)
        self.booking = Booking.objects.create(
            name='Jane Doe',
            no_of_guests=2,
            booking_date=self.booking_time,
        )

    def test_bookings_list_unauthenticated_rejected(self):
        """Secured table booking API returns 401 when accessed without token."""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bookings_list_authenticated_succeeds(self):
        """Authenticated client with Token receives 200 OK and bookings list."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jane Doe')

    def test_booking_post_authenticated(self):
        """Authenticated client can insert booking data into database via API."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        payload = {
            'name': 'John Smith',
            'no_of_guests': 6,
            'booking_date': '2026-11-20T19:30:00Z',
        }
        response = self.client.post('/api/bookings/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(name='John Smith').exists())


class UserRegistrationApiTest(TestCase):
    """
    Unit test for User Registration endpoint.
    """

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_via_api(self):
        payload = {
            'username': 'newcustomer',
            'email': 'newcustomer@example.com',
            'password': 'StrongPassword2026!',
        }
        response = self.client.post('/api/registration/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newcustomer').exists())


class StaticContentPagesTest(TestCase):
    """
    Unit tests verifying that the web application uses Django to serve static HTML content.
    """

    def test_home_page_served_with_static_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'SPECIAL OFFER')
        self.assertContains(response, 'static/img/logo.png')

    def test_about_page_served(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_menu_page_served(self):
        Menu.objects.create(title='Greek Salad', price=12, inventory=10)
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertContains(response, 'Greek Salad')

    def test_book_page_served(self):
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')
        self.assertContains(response, 'Make a reservation')

    def test_reservations_page_served(self):
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_register_page_served(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

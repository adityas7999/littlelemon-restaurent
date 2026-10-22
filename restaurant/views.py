import json
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .forms import BookingForm
from .models import Booking, Menu, RESERVATION_SLOTS
from .serializers import (
    BookingSerializer,
    MenuSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


def _booking_records(bookings):
    records = []
    for b in bookings:
        records.append({
            'pk': b.id,
            'id': b.id,
            'name': b.name,
            'no_of_guests': b.no_of_guests,
            'booking_date': b.booking_date.isoformat() if b.booking_date else '',
            'fields': {
                'first_name': b.name,
                'reservation_date': (
                    b.booking_date.date().isoformat() if b.booking_date else ''
                ),
                'reservation_slot': b.booking_date.hour if b.booking_date else 10,
            },
        })
    return records


# ==============================================================================
# Static & HTML Template Views
# ==============================================================================


def home(request):
    """Serve home page with static HTML content."""
    return render(request, 'index.html')


def about(request):
    """Serve static about page."""
    return render(request, 'about.html')


def reservations(request):
    """Display all reservations page."""
    bookings = Booking.objects.all().order_by('booking_date')
    return render(
        request,
        'bookings.html',
        {'bookings': _booking_records(bookings)},
    )


def book(request):
    """Interactive table reservation form page."""
    return render(
        request,
        'book.html',
        {
            'today': timezone.localdate(),
            'reservation_slots': RESERVATION_SLOTS,
        },
    )


def menu(request):
    """Menu browsing page."""
    return render(request, 'menu.html', {'menu_items': Menu.objects.all()})


def display_menu_item(request, pk):
    """Single menu item view."""
    menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {'menu_item': menu_item})


def register_page(request):
    """HTML user registration page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f'Account successfully created for {user.username}! You can now log in.'
            )
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def bookings_api(request):
    """AJAX endpoint for the booking calendar in book.html."""
    if request.method == 'GET':
        date_text = request.GET.get('date')
        bookings = Booking.objects.all().order_by('booking_date')
        if date_text:
            parsed = parse_date(date_text)
            if parsed is None:
                return JsonResponse(
                    {'error': 'Use a valid date in YYYY-MM-DD format.'},
                    status=400,
                )
            bookings = bookings.filter(
                booking_date__year=parsed.year,
                booking_date__month=parsed.month,
                booking_date__day=parsed.day,
            )

        return HttpResponse(
            json.dumps(_booking_records(bookings)),
            content_type='application/json',
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Request body must contain valid JSON.'},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {'error': 'Send the reservation as a JSON object.'},
            status=400,
        )

    form = BookingForm(data)
    if not form.is_valid():
        return JsonResponse(
            {'errors': form.errors.get_json_data()},
            status=400,
        )

    # Check for slot conflicts
    cleaned_date = form.cleaned_data['booking_date']
    if Booking.objects.filter(booking_date=cleaned_date).exists():
        return JsonResponse(
            {'error': 'That time has already been booked for this date.'},
            status=400,
        )

    try:
        with transaction.atomic():
            booking = form.save()
    except IntegrityError:
        return JsonResponse(
            {'error': 'That time has already been booked for this date.'},
            status=400,
        )

    return JsonResponse(_booking_records([booking])[0], status=201)


# ==============================================================================
# Django REST Framework (DRF) API Views
# ==============================================================================


class MenuItemsView(generics.ListCreateAPIView):
    """
    API endpoint for listing all menu items (GET) or creating a new one (POST).
    GET is public. POST requires token authentication.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


# Alias for backward-compatibility with lab naming
MenuItemView = MenuItemsView


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a single menu item.
    GET is public. PUT/PATCH/DELETE require token authentication.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing table reservations (bookings).
    Fully secured with Token Authentication (requires IsAuthenticated).
    """
    queryset = Booking.objects.all().order_by('booking_date')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration via JSON POST /api/registration/.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for listing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

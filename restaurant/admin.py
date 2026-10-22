from django.contrib import admin

from .models import Booking, Menu


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'no_of_guests', 'booking_date')
    list_filter = ('booking_date',)
    search_fields = ('name',)
    ordering = ('booking_date',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'inventory')
    list_filter = ('price',)
    search_fields = ('title',)

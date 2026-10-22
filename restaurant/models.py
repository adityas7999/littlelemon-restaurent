from django.db import models


def _time_label(hour):
    hour_12 = hour % 12 or 12
    period = 'AM' if hour < 12 else 'PM'
    return f'{hour_12} {period}'


RESERVATION_SLOTS = tuple(
    (hour, _time_label(hour)) for hour in range(10, 21)
)


class Menu(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    inventory = models.IntegerField(default=5)
    description = models.TextField(max_length=1000, default='', blank=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f'{self.title} : {str(self.price)}'

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

    @property
    def menu_item_description(self):
        return self.description

    @menu_item_description.setter
    def menu_item_description(self, value):
        self.description = value


# Alias MenuItem to Menu for cross-compatibility with Capstone lab references
MenuItem = Menu


class Booking(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    no_of_guests = models.IntegerField(default=1)
    booking_date = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ('booking_date',)

    def __str__(self):
        return f'{self.name} : {str(self.booking_date)}'

    @property
    def first_name(self):
        return self.name

    @first_name.setter
    def first_name(self, value):
        self.name = value

    @property
    def reservation_date(self):
        return self.booking_date.date() if self.booking_date else None

    @property
    def reservation_slot(self):
        return self.booking_date.hour if self.booking_date else 10

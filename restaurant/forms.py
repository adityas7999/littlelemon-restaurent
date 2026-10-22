from datetime import datetime, time
from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200, required=False)
    reservation_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    reservation_slot = forms.IntegerField(required=False, initial=10)

    class Meta:
        model = Booking
        fields = ('name', 'no_of_guests', 'booking_date')
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        name = cleaned_data.get('name')
        res_date = cleaned_data.get('reservation_date')
        res_slot = cleaned_data.get('reservation_slot')
        b_date = cleaned_data.get('booking_date')

        if not name and first_name:
            cleaned_data['name'] = first_name
            self.instance.name = first_name

        if not b_date and res_date and res_slot is not None:
            combined = datetime.combine(res_date, time(hour=int(res_slot), minute=0))
            cleaned_data['booking_date'] = combined
            self.instance.booking_date = combined

        if not cleaned_data.get('name'):
            raise forms.ValidationError('Name is required.')
        if not cleaned_data.get('booking_date'):
            raise forms.ValidationError('Booking date and time are required.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['name']
        instance.booking_date = self.cleaned_data['booking_date']
        if not instance.no_of_guests:
            instance.no_of_guests = 1
        if commit:
            instance.save()
        return instance

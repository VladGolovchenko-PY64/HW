from django import forms
from .models import Reservation
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'hour_start', 'hour_end']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

        today = timezone.now().date()
        self.fields['date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'min': today.strftime('%Y-%m-%d')
            }
        )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("Нельзя бронировать на прошлую дату!")
        return date

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        hour_start = cleaned_data.get('hour_start')
        hour_end = cleaned_data.get('hour_end')

        if table and date:

            exists = Reservation.objects.filter(
                table=table,
                date=date,
                hour_start__lt=hour_end,
                hour_end__gt=hour_start
            ).exists()
            if exists:
                raise forms.ValidationError("Этот столик уже забронирован на это время.")


            if self.user:
                user_bookings_today = Reservation.objects.filter(
                    user=self.user,
                    date=date
                ).count()
                if user_bookings_today >= 1:
                    raise forms.ValidationError("Вы уже бронировали столик на этот день.")

        return cleaned_data

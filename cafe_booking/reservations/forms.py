from django import forms
from datetime import date
from .models import Reservation

OPEN_HOUR = 8
CLOSE_HOUR = 18

class ReservationForm(forms.ModelForm):
    hour_start = forms.ChoiceField(
        choices=[(h, f'{h}:00') for h in range(OPEN_HOUR, CLOSE_HOUR)],
        label="С"
    )
    hour_end = forms.ChoiceField(
        choices=[(h, f'{h}:00') for h in range(OPEN_HOUR + 1, CLOSE_HOUR + 1)],
        label="По"
    )

    class Meta:
        model = Reservation
        fields = ['table', 'date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError("Нельзя бронировать в прошлом.")
        return d

    def clean(self):
        cleaned = super().clean()
        table = cleaned.get('table')
        date_ = cleaned.get('date')
        start = int(cleaned.get('hour_start'))
        end   = int(cleaned.get('hour_end'))

        if start >= end:
            raise forms.ValidationError("Время окончания должно быть больше времени начала.")

        from .models import Reservation

        if Reservation.objects.filter(user=self.user, date=date_).exists():
            raise forms.ValidationError("У вас уже есть бронь на этот день.")


        overlapping = Reservation.objects.filter(
            table=table,
            date=date_,
            hour_start__lt=end,
            hour_end__gt=start
        )
        if overlapping.exists():
            raise forms.ValidationError("Этот столик уже занят в выбранный интервал.")
        return cleaned

from django import forms
from .models import Reservation
from datetime import date

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["table", "date", "hour_start", "hour_end"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # ограничение времени
        self.fields["hour_start"].widget = forms.NumberInput(attrs={"min": 8, "max": 18})
        self.fields["hour_end"].widget = forms.NumberInput(attrs={"min": 8, "max": 18})

        # выбор даты через календарь
        self.fields["date"].widget = forms.DateInput(attrs={"type": "date"})

    def clean(self):
        cleaned = super().clean()
        table = cleaned.get("table")
        date_ = cleaned.get("date")
        start = cleaned.get("hour_start")
        end = cleaned.get("hour_end")

        if not (table and date_ and start and end):
            return cleaned

        # прошлое время
        if date_ < date.today():
            raise forms.ValidationError("Нельзя бронировать столик на прошлую дату.")

        # проверка на диапазон
        if start < 8 or end > 18 or start >= end:
            raise forms.ValidationError("Время бронирования должно быть с 8:00 до 18:00.")

        # одна бронь в день
        if self.user and Reservation.objects.filter(user=self.user, date=date_).exists():
            raise forms.ValidationError("Вы можете забронировать только один столик на этот день.")

        # проверка пересечений
        overlapping = Reservation.objects.filter(
            table=table,
            date=date_,
            hour_start__lt=end,
            hour_end__gt=start
        )
        if overlapping.exists():
            raise forms.ValidationError("Этот столик уже занят в выбранный интервал.")

        return cleaned

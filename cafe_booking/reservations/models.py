from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    image = models.ImageField(upload_to="tables/", blank=True, null=True)

    def __str__(self):
        return f"Столик {self.number} ({self.seats} мест)"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    date = models.DateField()
    hour_start = models.IntegerField()
    hour_end = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронь {self.table} от {self.user} на {self.date} ({self.hour_start}-{self.hour_end})"

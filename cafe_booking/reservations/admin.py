from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')
    list_filter = ('seats',)
    search_fields = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('table', 'user', 'date', 'hour_start', 'hour_end', 'created_at')
    list_filter = ('date', 'table', 'user')
    search_fields = ('table__number', 'user__username')

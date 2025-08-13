from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Table, Reservation
from .forms import ReservationForm

def home(request):
    return render(request, 'home.html')

def tables_list(request):
    seats_filter = request.GET.get('seats')
    tables = Table.objects.all()
    if seats_filter:
        try:
            seats_int = int(seats_filter)
            tables = tables.filter(seats=seats_int)
        except ValueError:
            pass
    return render(request, 'tables_list.html', {'tables': tables})

@login_required
def new_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm(user=request.user)
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-hour_start')
    return render(request, 'my_reservations.html', {'reservations': reservations})

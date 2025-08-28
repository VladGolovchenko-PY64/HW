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
            val = int(seats_filter)
            low = max(1, val)
            high = val + 2
            tables = tables.filter(seats__gte=low, seats__lte=high)
        except ValueError:
            pass
    return render(request, 'tables_list.html', {'tables': tables})

@login_required
def new_reservation(request):
    table_id = request.GET.get('table_id')
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
    else:
        initial = {}
        if table_id:
            initial['table'] = get_object_or_404(Table, id=table_id)
        form = ReservationForm(user=request.user, initial=initial)

    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = request.user
        reservation.save()
        return redirect('my_reservations')

    return render(request, 'reservation_form.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-hour_start')
    return render(request, 'my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('my_reservations')

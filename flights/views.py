from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Airport, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    if Flight.objects.get(pk=flight_id).exists():
        return render (request, "flights/flight.html", {
            "flight": flight,
            # Related key (allows reverse search)
            "passengers": flight.passengers.all(),
            # Non-passenger context for people who are not on the flight
            "non_passengers": Passenger.objects.exclude(flights=flight).all()
        })
    else:
        return render(request, "flights/flight.html", {
            "flight": "There are no flights with this ID"
        })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        # Reverse gets the route from views from the url name
        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))


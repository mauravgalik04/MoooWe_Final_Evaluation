import os
from django.shortcuts import render,redirect,get_object_or_404
from Movies.models import Movie
from django.conf import settings
from Bookings.models import Theatre , Show
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# Create your views here.
@login_required 
def booking_home_view(request):
    theatres = Theatre.objects.all()
    shows = Show.objects.all()
    query = request.GET.get('searchbar')
    if query:
        movies = Movie.objects.filter(name__icontains=query)
    else:
        movies = Movie.objects.all()
    data = {"movies": movies ,"theatres":theatres , "shows":shows}
    return render(request, 'booking_home_page.html', context=data)
@login_required 
def theater_dashboard_view(request):
    theatres = Theatre.objects.all()
    data = {"theatres" : theatres}
    return render(request , 'theatre_dashboard.html' , context=data)
@login_required 
def register_theatre_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        theatre = Theatre.objects.create(
            image=image,
            name=request.POST.get('theatre-name'),
            location=request.POST.get('location'),
            capacity=request.POST.get('capacity'),
            gold_seats=request.POST.get('gold-seats'),
            gold_price=request.POST.get('gold-price'),
            silver_seats=request.POST.get('silver-seats'),
            silver_price=request.POST.get('silver-price'),
            bronze_seats=request.POST.get('bronze-seats'),
            bronze_price=request.POST.get('bronze-price'),
            owner_id=request.user.id
        )
        messages.success(request , "Theatre added successfully!")
    return render(request, 'theatre_registration.html')
@login_required 
def update_theatre_view(request , id):
    theatre = get_object_or_404(Theatre, id=id)
    if request.method == "POST":
        theatre.image = request.FILES.get('image')
        theatre.name = request.POST.get('theatre-name')
        theatre.location=request.POST.get('location'),
        theatre.capacity=request.POST.get('capacity'),
        theatre.gold_seats=request.POST.get('gold-seats'),
        theatre.gold_price=request.POST.get('gold-price'),
        theatre.silver_seats=request.POST.get('silver-seats'),
        theatre.silver_price=request.POST.get('silver-price'),
        theatre.bronze_seats=request.POST.get('bronze-seats'),
        theatre.bronze_price=request.POST.get('bronze-price'),
        theatre.owner_id=request.user.id
        theatre.save()
        messages.success(request , "Theatre updated successfully!")
        return redirect('theatre_dashboard')
    data = {"theatre" : theatre}
    return render(request , 'update_theatre.html' , context = data)
@login_required 
def delete_theatre_view(request , id):
    theatre = Theatre.objects.filter(id = id)
    theatre.delete()
    messages.success(request , "Theatre deleted!!")
    return redirect('theatre_dashboard')
@login_required 
def add_show_view(request , id):
    t_id = id
    if request.method=="POST":
        show = Show.objects.create(
        movie_name=request.POST.get('movie_name'),
        duration=request.POST.get('duration'),
        time=request.POST.get('show_time'),
        date=request.POST.get('show_date'),
        movie_poster=request.FILES.get('movie_poster'),
        theatre_id=t_id
        )
        messages.success(request , "Show added!!")
        return redirect('theatre_dashboard')
    return render(request , 'add_show.html')
@login_required 
def manage_show_view(request , id):
    t_id = id
    shows = Show.objects.filter(theatre_id = t_id)
    data = {"shows" : shows}
    return render(request , 'manage_show.html',context=data)
@login_required 
def update_show_view(request , id):
    show =  get_object_or_404(Show, id=id)
    data = {"show":show}
    if request.method == "POST":
        movie_name=request.POST.get('movie_name'),
        duration=request.POST.get('duration'),
        time=request.POST.get('show_time'),
        date=request.POST.get('show_date'),
        movie_poster=request.FILES.get('movie_poster')
        show.save()
        messages.success(request , "Show updated successfully!!")
        return redirect('theatre_dashboard')
    return render(request , "update_show.html" , context=data)
@login_required 
def delete_show_view(request , id):
    show = Show.objects.filter(id = id)
    show.delete()
    messages.success(request , "Show deleted!!")
    return redirect('theatre_dashboard')

@login_required
def book_show(request , theatre_id):
    theatre = Theatre.objects.get(id=theatre_id)
    data = {
    'theatre': theatre,
    'gold_range': range(theatre.gold_seats),
    'silver_range': range(theatre.silver_seats),
    'bronze_range': range(theatre.bronze_seats),
}
    return render(request , 'theatre.html',context=data)
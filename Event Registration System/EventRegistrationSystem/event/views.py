from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event, Registration
from .forms import UserRegistrationForm, EventRegistrationForm, EventCreationForm

def home(request):
    events = Event.objects.all().order_by('-date', '-time')
    context = {
        'events': events,
        'is_staff': request.user.is_staff
    }
    return render(request, 'event/home.html', context)

@staff_member_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventCreationForm()
    
    return render(request, 'event/create_event.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'event/register.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
        'available_tickets': event.max_tickets - event.tickets_sold
    }
    return render(request, 'event/event_detail.html', context)

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, event=event)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.total_price = event.price * registration.number_of_tickets
            registration.save()
            
            event.tickets_sold += registration.number_of_tickets
            event.save()
            
            messages.success(request, 'Successfully registered for the event!')
            return redirect('my_registrations')
    else:
        form = EventRegistrationForm(event=event)
    
    context = {
        'form': form,
        'event': event
    }
    return render(request, 'event/register_for_event.html', context)

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'event/my_registrations.html', {'registrations': registrations})

@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if registration.status != 'cancelled':
        registration.status = 'cancelled'
        registration.event.tickets_sold -= registration.number_of_tickets
        registration.event.save()
        registration.save()
        messages.success(request, 'Registration cancelled successfully!')
    return redirect('my_registrations')

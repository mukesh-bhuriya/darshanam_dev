from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from .models import Temple, Muhurat, Category, Event, Booking, Donation, Wishlist, KarmaPoints, LanguagePreference, DonorWall
from adminpanel.models import Temple, Muhurat, Category, Event  # models from admin app
from .models import Booking, Donation, Wishlist, KarmaPoints, LanguagePreference, DonorWall  # models from frontend app
from .forms import DevoteeRegisterForm

def about_view(request):
    return render(request, 'frontend/pages/about.html')

def home_view(request):
    # Get featured temples
    featured_temples = Temple.objects.filter(is_featured=True)[:3]
    
    # Get today's muhurats
    today = date.today()
    muhurats = Muhurat.objects.filter(date=today)
    
    # Get all categories
    categories = Category.objects.all()[:8]
    
    # Get active events
    events = Event.objects.filter(is_active=True, end_date__gte=today).order_by('start_date')[:5]
    
    context = {
        'featured_temples': featured_temples,
        'muhurats': muhurats,
        'categories': categories,
        'events': events
    }
    return render(request, 'frontend/pages/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or wherever you want to send them
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'frontend/pages/login.html')

def register_view(request):
    if request.method == 'POST':
        form = DevoteeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('user_login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DevoteeRegisterForm()

    return render(request, 'frontend/pages/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    # Temple onboarding data
    temples = []  # Replace with actual temple query
    
    # Product management data
    products = []  # Replace with actual product query
    
    # Booking/order management data
    bookings = []  # Replace with actual booking query
    
    # Donation reports data
    donations = []  # Replace with actual donation query
    total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Monthly donations (last 30 days)
    monthly_donations = donations.filter(
        date__gte=datetime.now() - timedelta(days=30)
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Top donors (top 5)
    top_donors = donations.values('donor_name').annotate(
        amount=Sum('amount')
    ).order_by('-amount')[:5]
    
    # Analytics data
    visitor_stats = []  # Replace with actual analytics query
    revenue_stats = []  # Replace with actual revenue query
    temple_visits = []  # Replace with actual temple visits query
    
    context = {
        'temples': temples,
        'products': products,
        'bookings': bookings,
        'donations': donations,
        'total_donations': total_donations,
        'monthly_donations': monthly_donations,
        'top_donors': top_donors,
        'visitor_stats': visitor_stats,
        'revenue_stats': revenue_stats,
        'temple_visits': temple_visits
    }
    
    return render(request, 'frontend/pages/admin_panel.html', context)
    # Get featured temples
    featured_temples = Temple.objects.filter(is_featured=True)[:3]
    
    # Get today's muhurats
    today = date.today()
    muhurats = Muhurat.objects.filter(date=today)
    
    # Get all categories
    categories = Category.objects.all()[:8]
    
    # Get active events
    events = Event.objects.filter(is_active=True, end_date__gte=today).order_by('start_date')[:5]
    
    context = {
        'featured_temples': featured_temples,
        'muhurats': muhurats,
        'categories': categories,
        'events': events
    }
    return render(request, 'frontend/pages/index.html', context)

@login_required
def dashboard_view(request):
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    
    # Get user's donations
    donations = Donation.objects.filter(user=request.user).order_by('-date')
    
    # Get user's wishlist items
    wishlist = Wishlist.objects.filter(user=request.user)
    
    # Get user's karma points
    # karma_points = KarmaPoints.objects.get_or_create(user=request.user)[0]
    karma_points, _ = KarmaPoints.objects.get_or_create(user=request.user)
    
    context = {
        'bookings': bookings,
        'donations': donations,
        'wishlist': wishlist,
        'karma_points': karma_points
    }
    return render(request, 'frontend/pages/dashboard.html', context)

@login_required
def set_language_preference(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        LanguagePreference.objects.update_or_create(
            user=request.user,
            defaults={'language': language}
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_ai_recommendations(request):
    # TODO: Implement AI recommendation logic
    return JsonResponse({'recommendations': []})

@login_required
def get_temple_map_data(request):
    temples = Temple.objects.values('id', 'name', 'latitude', 'longitude', 'deity')
    return JsonResponse({'temples': list(temples)})

@login_required
def get_festival_countdowns(request):
    upcoming_events = Event.objects.filter(
        is_active=True,
        end_date__gte=date.today()
    ).order_by('start_date').values('id', 'name', 'start_date')
    return JsonResponse({'events': list(upcoming_events)})

@login_required
def get_donor_wall(request, temple_id):
    donors = DonorWall.objects.filter(
        temple_id=temple_id
    ).order_by('-amount')[:10]
    return JsonResponse({'donors': list(donors.values())})

@login_required
def my_bookings_view(request):
    bookings = request.user.bookings.all()
    return render(request, 'frontend/my_bookings.html', {'bookings': bookings})

@login_required
def wishlist_view(request):
    wishlist = request.user.wishlist.all()
    return render(request, 'frontend/wishlist.html', {'wishlist': wishlist})

@login_required
def donations_view(request):
    donations = request.user.donations.all()
    return render(request, 'frontend/donations.html', {'donations': donations})

@login_required
def events_view(request):
    # Get upcoming events
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'frontend/events.html', {'events': events})

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    return render(request, 'frontend/notifications.html', {'notifications': notifications})

@login_required
def account_settings_view(request):
    # Handle account settings form
    return render(request, 'frontend/account_settings.html')
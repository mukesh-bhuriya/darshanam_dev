from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from .models import Temple, Muhurat, Category, Event, Booking, Donation, Wishlist, KarmaPoints, LanguagePreference, DonorWall
from adminpanel.models import Temple, Muhurat, Category, Event  # models from admin app
from .models import Booking, Donation, Wishlist, KarmaPoints, LanguagePreference, DonorWall  # models from frontend app

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
    karma_points = KarmaPoints.objects.get_or_create(user=request.user)[0]
    
    context = {
        'bookings': bookings,
        'donations': donations,
        'wishlist': wishlist,
        'karma_points': karma_points
    }
    return render(request, 'dashboard.html', context)

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
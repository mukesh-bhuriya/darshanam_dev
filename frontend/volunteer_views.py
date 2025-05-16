from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Temple, Event
from .integrations import (
    LiveStreamIntegration,
    AIChatbotIntegration,
    TranslationIntegration,
    AstrologyIntegration,
    PaymentIntegration,
    ARVRIntegration
)

@login_required
def volunteer_portal(request):
    """
    Main view for volunteer portal with integration support
    """
    nearby_temples = Temple.objects.all()  # TODO: Add location filtering
    upcoming_events = Event.objects.filter(
        is_active=True,
        end_date__gte=datetime.now()
    ).order_by('start_date')
    
    # Initialize integrations
    integrations = {
        'live_stream': LiveStreamIntegration(),
        'chatbot': AIChatbotIntegration(),
        'translation': TranslationIntegration(),
        'astrology': AstrologyIntegration(),
        'payment': PaymentIntegration(),
        'ar_vr': ARVRIntegration()
    }
    
    context = {
        'nearby_temples': nearby_temples,
        'upcoming_events': upcoming_events,
        'integrations': integrations
    }
    return render(request, 'frontend/pages/volunteer_portal.html', context)

@login_required
def get_volunteer_opportunities(request, temple_id):
    """
    Returns volunteer opportunities for a specific temple
    """
    opportunities = []  # TODO: Implement opportunity retrieval
    return JsonResponse({'opportunities': opportunities})

@login_required
def register_volunteer(request):
    """
    Handles volunteer registration
    """
    if request.method == 'POST':
        # TODO: Implement volunteer registration
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.models import User
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'adminlte/pages/examples/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data.get('email', '')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'adminlte/pages/examples/register.html', {'form': form})

def otp_verification_view(request):
    return redirect('home')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))
            request.session['reset_otp'] = otp
            request.session['reset_user_id'] = user.id
            
            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user with this email exists')
    return render(request, 'adminlte/pages/examples/forgot-password.html')

def reset_password_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if otp == request.session.get('reset_otp'):
            if new_password == confirm_password:
                user = User.objects.get(id=request.session.get('reset_user_id'))
                user.set_password(new_password)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'adminlte/pages/examples/reset-password.html')

def home_view(request):
    # Get featured temples
    featured_temples = Temple.objects.filter(is_featured=True)[:3]
    
    # Get today's muhurats
    from datetime import date
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
    return render(request, 'adminlte/pages/index.html', context)

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    """Model for temple categories"""
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('Slug'))  # added slug
    description = models.TextField(blank=True, verbose_name=_('Description'))
    image = models.ImageField(upload_to='categories/', verbose_name=_('Image'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

class Temple(models.Model):
    """Model for temple listings"""
    name = models.CharField(max_length=200, verbose_name=_('Temple Name'))
    description = models.TextField(verbose_name=_('Description'))
    featured_image = models.ImageField(upload_to='temples/', verbose_name=_('Featured Image'))
    gallery_images = models.JSONField(default=list, verbose_name=_('Gallery Images'))
    location = models.CharField(max_length=200, verbose_name=_('Location'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    google_map_url = models.URLField(blank=True, verbose_name=_('Google Map URL'))
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Temple')
        verbose_name_plural = _('Temples')

    def __str__(self):
        return self.name

class Muhurat(models.Model):
    """Model for auspicious timings"""
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    date = models.DateField(verbose_name=_('Date'))
    time = models.TimeField(verbose_name=_('Time'))
    importance = models.CharField(max_length=100, verbose_name=_('Importance'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Muhurat')
        verbose_name_plural = _('Muhurats')

class Horoscope(models.Model):
    """Model for horoscope analysis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zodiac_sign = models.CharField(max_length=50, blank=True)
    date_range = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)  # Add if needed
    birth_date = models.DateField(verbose_name=_('Birth Date'))
    birth_time = models.TimeField(verbose_name=_('Birth Time'))
    birth_place = models.CharField(max_length=255, verbose_name=_('Birth Place'))
    analysis = models.TextField(verbose_name=_('Analysis'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Horoscope')
        verbose_name_plural = _('Horoscopes')

    def __str__(self):
        return f"{self.user.username}'s Horoscope"

class Compatibility(models.Model):
    """Model for compatibility analysis"""
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_compatibility')
    user_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('User Gender'))
    partner_birth_date = models.DateField(verbose_name=_('Partner Birth Date'))
    partner_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('Partner Gender'))
    compatibility_score = models.IntegerField(verbose_name=_('Compatibility Score'))
    analysis = models.TextField(verbose_name=_('Analysis'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Compatibility')
        verbose_name_plural = _('Compatibilities')

    def __str__(self):
        return f"{self.user.username}'s Compatibility Analysis"

class Astrologer(models.Model):
    """Model for astrologer profiles"""
    CONSULTATION_TYPES = [
        ('chat', _('Chat Consultation')),
        ('voice', _('Voice Call')),
        ('video', _('Video Call')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    specialization = models.CharField(max_length=255, verbose_name=_('Specialization'))
    experience = models.IntegerField(verbose_name=_('Experience (years)'))
    rating = models.FloatField(verbose_name=_('Rating'))
    reviews = models.IntegerField(verbose_name=_('Reviews'))
    price_chat = models.IntegerField(verbose_name=_('Chat Price (₹)'))
    price_voice = models.IntegerField(verbose_name=_('Voice Price (₹)'))
    price_video = models.IntegerField(verbose_name=_('Video Price (₹)'))
    chat_rate_per_min = models.IntegerField(verbose_name=_('Chat Rate Per Minute (₹)'), default=10)
    call_rate_per_min = models.IntegerField(verbose_name=_('Call Rate Per Minute (₹)'), default=20)
    photo = models.ImageField(upload_to='astrologers/', verbose_name=_('Photo'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Astrologer')
        verbose_name_plural = _('Astrologers')

    def __str__(self):
        return self.name

class Event(models.Model):
    """Model for events carousel"""
    title = models.CharField(max_length=200, verbose_name=_('Event Title'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='events/', verbose_name=_('Image'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return self.title

class PoojaService(models.Model):
    """Model for pooja services"""
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, verbose_name=_('Temple'))
    name = models.CharField(max_length=200, verbose_name=_('Service Name'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    duration = models.CharField(max_length=50, verbose_name=_('Duration'))
    is_available = models.BooleanField(default=True, verbose_name=_('Available'))

    class Meta:
        verbose_name = _('Pooja Service')
        verbose_name_plural = _('Pooja Services')

    def __str__(self):
        return f"{self.temple.name} - {self.name}"

class SiteSetting(models.Model):
    """Model for global site settings"""
    site_name = models.CharField(max_length=100, default='Darshanam', verbose_name=_('Site Name'))
    contact_email = models.EmailField(verbose_name=_('Contact Email'))
    maintenance_mode = models.BooleanField(default=False, verbose_name=_('Maintenance Mode'))
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name=_('Google Analytics ID'))

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Only one SiteSetting instance allowed, delete others on save
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

class HomepageContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Add this field
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

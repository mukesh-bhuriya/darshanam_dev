from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class KarmaPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Karma Points')
        verbose_name_plural = _('Karma Points')

    def __str__(self):
        return f"{self.user.username}'s Karma: {self.points}"

class LanguagePreference(models.Model):
    LANGUAGES = [
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('kn', 'Kannada'),
        ('ml', 'Malayalam'),
        ('en', 'English'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')

    class Meta:
        verbose_name = _('Language Preference')
        verbose_name_plural = _('Language Preferences')

    def __str__(self):
        return f"{self.user.username}'s Language: {self.get_language_display()}"

class DonorWall(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    temple = models.ForeignKey('adminpanel.Temple', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    message = models.TextField(blank=True)

    class Meta:

        verbose_name = _('Donor Wall Entry')
        verbose_name_plural = _('Donor Wall Entries')
        ordering = ['-date']

    def __str__(self):
        return f"{self.donor.username} donated {self.amount} to {self.temple.name}"


class Booking(models.Model):
    name = models.CharField(max_length=100)

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Wishlist(models.Model):
    item_name = models.CharField(max_length=100)

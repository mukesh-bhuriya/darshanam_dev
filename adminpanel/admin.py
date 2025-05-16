from django.contrib import admin
from .models import (
    HomepageContent,
    Temple,
    PoojaService,
    SiteSetting,
    Category,
    Muhurat,
    Event,
    Horoscope,
    Compatibility,
    Astrologer
)

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_featured', 'created_at')
    list_editable = ('is_featured',)
    list_filter = ('is_featured', 'categories')
    search_fields = ('name', 'location')
    filter_horizontal = ('categories',)


@admin.register(Muhurat)
class MuhuratAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'importance')
    list_filter = ('date', 'importance')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'


@admin.register(Horoscope)
class HoroscopeAdmin(admin.ModelAdmin):
    list_display = ('zodiac_sign', 'date_range', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'zodiac_sign')
    search_fields = ('title', 'description', 'zodiac_sign')

@admin.register(Compatibility)
class CompatibilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_gender', 'partner_birth_date', 'partner_gender', 'compatibility_score')
    # No 'is_active' field in your model, so remove it from editable and filter
    list_filter = ('user_gender', 'partner_gender', 'compatibility_score')
    search_fields = ('user__username', 'analysis')  # user is FK, so search by related user username and analysis text

@admin.register(Astrologer)
class AstrologerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'specialization', 'experience', 'rating', 'reviews')
        }),
        ('Pricing', {
            'fields': ('price_chat', 'price_voice', 'price_video', 'chat_rate_per_min', 'call_rate_per_min')
        }),
        ('Media', {
            'fields': ('photo',)
        }),
    )
    # list_display = ('name', 'specialization', 'experience', 'is_available', 'chat_rate_per_min', 'call_rate_per_min')
    # list_editable = ('is_available',)
    # list_filter = ('is_available', 'specialization')
    # search_fields = ('name', 'specialization', 'description')
    # filter_horizontal = ('languages',)
    list_display = ('name', 'specialization', 'experience', 'chat_rate_per_min', 'call_rate_per_min')
    list_filter = ('specialization',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'


@admin.register(PoojaService)
class PoojaServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'price', 'is_available')
    list_editable = ('is_available',)
    list_filter = ('is_available', 'temple')
    search_fields = ('name', 'description')
    raw_id_fields = ('temple',)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'maintenance_mode')
    list_editable = ('maintenance_mode',)

    def has_add_permission(self, request):
        # Only allow adding one SiteSetting instance
        return not SiteSetting.objects.exists()

from django.contrib import admin
from django import forms
from .models import (
    GlobalSettings, HeroSection, AboutSection, AboutGalleryImage,
    NewsItem, Publication, Member, Testimonial, MembershipRequest
)
from .forms import make_admin_image_url_form
import urllib.request
import imghdr


def fetch_image_from_url(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            # try to get mime from response headers
            ctype = None
            try:
                ctype = resp.headers.get_content_type()
            except Exception:
                ctype = resp.getheader('Content-Type') if hasattr(resp, 'getheader') else None
            if not ctype or ctype == 'application/octet-stream':
                ext = imghdr.what(None, data) or 'jpeg'
                ctype = f'image/{ext if ext != "jpg" else "jpeg"}'
            return data, ctype
    except Exception:
        return None, None


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_contact', 'phone', 'address')
    fieldsets = (
        ('Contact Information', {
            'fields': ('email_contact', 'phone', 'address')
        }),
    )


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    form = make_admin_image_url_form(HeroSection)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle')
        }),
        ('Image', {
            'fields': ('image_file', 'image_url_input'),
            'description': 'Upload an image (local) or provide a URL.'
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AboutGalleryImage)
class AboutGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    form = make_admin_image_url_form(AboutGalleryImage)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'order')
        }),
        ('Image', {
            'fields': ('image_file', 'image_url_input'),
            'description': 'Upload an image (local) or provide a URL.'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    ordering = ('order',)

    def save_model(self, request, obj, form, change):
        # prefer a pasted URL, then a local uploaded file
        if form is not None:
            image_url = form.cleaned_data.get('image_url_input') if hasattr(form, 'cleaned_data') else None
            image_file = form.cleaned_data.get('image_file') if hasattr(form, 'cleaned_data') else None
        else:
            image_url = request.POST.get('image_url_input')
            image_file = request.FILES.get('image_file')

        if image_url:
            data, mime = fetch_image_from_url(image_url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime

        elif image_file:
            try:
                data = image_file.read()
                obj.image_blob = data
                ext = imghdr.what(None, data) or 'jpeg'
                obj.image_blob_mime = f'image/{ext if ext!='jpg' else "jpeg"}'
            except Exception:
                pass

        super().save_model(request, obj, form, change)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_str', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    form = make_admin_image_url_form(NewsItem)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'category', 'date_str')
        }),
        ('Image', {
            'fields': ('image_file', 'image_url_input')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # support URL or uploaded file
        image_url = form.cleaned_data.get('image_url_input') if form and hasattr(form, 'cleaned_data') else request.POST.get('image_url_input')
        image_file = form.cleaned_data.get('image_file') if form and hasattr(form, 'cleaned_data') else request.FILES.get('image_file')
        if image_url:
            data, mime = fetch_image_from_url(image_url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
        elif image_file:
            data = image_file.read()
            obj.image_blob = data
            ext = imghdr.what(None, data) or 'jpeg'
            obj.image_blob_mime = f'image/{ext if ext!='jpg' else "jpeg"}'
        super().save_model(request, obj, form, change)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_str', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    form = make_admin_image_url_form(Publication)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'category', 'date_str')
        }),
        ('Image', {
            'fields': ('image_file', 'image_url_input')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        image_url = form.cleaned_data.get('image_url_input') if form and hasattr(form, 'cleaned_data') else request.POST.get('image_url_input')
        image_file = form.cleaned_data.get('image_file') if form and hasattr(form, 'cleaned_data') else request.FILES.get('image_file')
        if image_url:
            data, mime = fetch_image_from_url(image_url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
        elif image_file:
            data = image_file.read()
            obj.image_blob = data
            ext = imghdr.what(None, data) or 'jpeg'
            obj.image_blob_mime = f'image/{ext if ext!='jpg' else "jpeg"}'
        super().save_model(request, obj, form, change)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'role', 'is_active', 'order')
    list_filter = ('is_active', 'role', 'created_at')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'position', 'email')
    form = make_admin_image_url_form(Member)
    fieldsets = (
        ('Information personnelle', {
            'fields': ('name', 'position', 'role', 'email', 'description')
        }),
        ('Photo', {
            'fields': ('photo_file', 'photo_url_input')
        }),
        ('Réseaux sociaux', {
            'fields': ('linkedin', 'twitter', 'facebook'),
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'name')

    def save_model(self, request, obj, form, change):
        photo_url = form.cleaned_data.get('photo_url_input') if form and hasattr(form, 'cleaned_data') else request.POST.get('photo_url_input')
        photo_file = form.cleaned_data.get('photo_file') if form and hasattr(form, 'cleaned_data') else request.FILES.get('photo_file')
        if photo_url:
            data, mime = fetch_image_from_url(photo_url)
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
        elif photo_file:
            data = photo_file.read()
            obj.photo_blob = data
            ext = imghdr.what(None, data) or 'jpeg'
            obj.photo_blob_mime = f'image/{ext if ext!='jpg' else "jpeg"}'
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'role', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'order')
    search_fields = ('author', 'role', 'quote')
    form = make_admin_image_url_form(Testimonial)
    fieldsets = (
        ('Contenu', {
            'fields': ('quote', 'author', 'role')
        }),
        ('Photo', {
            'fields': ('photo_file', 'photo_url_input')
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    ordering = ('order',)

    def save_model(self, request, obj, form, change):
        photo_url = form.cleaned_data.get('photo_url_input') if form and hasattr(form, 'cleaned_data') else request.POST.get('photo_url_input')
        photo_file = form.cleaned_data.get('photo_file') if form and hasattr(form, 'cleaned_data') else request.FILES.get('photo_file')
        if photo_url:
            data, mime = fetch_image_from_url(photo_url)
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
        elif photo_file:
            data = photo_file.read()
            obj.photo_blob = data
            ext = imghdr.what(None, data) or 'jpeg'
            obj.photo_blob_mime = f'image/{ext if ext!='jpg' else "jpeg"}'
        super().save_model(request, obj, form, change)


@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'profil', 'niveau', 'pays', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'profil', 'niveau', 'pays')
    search_fields = ('nom_complet', 'email', 'organisation', 'domaine', 'pays')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom_complet', 'email', 'telephone')
        }),
        ('Informations professionnelles', {
            'fields': ('profil', 'organisation', 'domaine', 'niveau', 'niveau_autre', 'pays', 'pays_autre')
        }),
        ('Candidature', {
            'fields': ('motivation', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

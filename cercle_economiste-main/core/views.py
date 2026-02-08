
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import *
from .forms import ContactForm, MembershipRequestForm
import imghdr


def blob_image(request, model, pk, field):
    # Serve binary image stored in DB for model/field
    model_map = {
        'aboutgalleryimage': AboutGalleryImage,
        'aboutsection': AboutSection,
        'herosection': HeroSection,
        'newsitem': NewsItem,
        'publication': Publication,
        'member': Member,
        'testimonial': Testimonial,
    }
    Model = model_map.get(model.lower())
    if not Model:
        raise Http404()
    obj = get_object_or_404(Model, pk=pk)
    blob_field = None
    mime = None
    if field == 'image' and hasattr(obj, 'image_blob'):
        blob_field = obj.image_blob
        mime = obj.image_blob_mime
    if field == 'photo' and hasattr(obj, 'photo_blob'):
        blob_field = obj.photo_blob
        mime = obj.photo_blob_mime
    if not blob_field:
        raise Http404()
    data = blob_field
    if not mime:
        ext = imghdr.what(None, data) or 'jpeg'
        mime = f'image/{ext if ext!='jpg' else "jpeg"}'
    return HttpResponse(data, content_type=mime)

def get_image_url(obj, image_field_name='image'):
    """Helper to get image URL from either image field or image_url fallback"""
    # If there's a blob field, return URL to serve it
    blob_attr = f'{image_field_name}_blob'
    blob_mime = f'{image_field_name}_blob_mime'
    if hasattr(obj, blob_attr) and getattr(obj, blob_attr):
        # build URL to blob view
        model_name = obj.__class__.__name__.lower()
        # map class name to route key used in blob_image
        key = model_name
        return reverse('blob_image', args=[key, obj.pk, image_field_name])

    image_field = getattr(obj, image_field_name, None)
    if image_field and hasattr(image_field, 'url') and image_field.url:
        return image_field.url
    return getattr(obj, f'{image_field_name}_url', '')

def get_common_context():
    settings = GlobalSettings.objects.first()
    if not settings:
        settings = GlobalSettings.objects.create()
    return {'settings': settings}

def index(request):
    ctx = get_common_context()
    hero = HeroSection.objects.first()
    if hero:
        hero.image_url = get_image_url(hero, 'image')
    
    about = AboutSection.objects.first()
    news = NewsItem.objects.filter().all()[:4]
    for item in news:
        item.image_url = get_image_url(item, 'image')
    
    publications = Publication.objects.filter().all()[:4]
    for item in publications:
        item.image_url = get_image_url(item, 'image')
    
    testimonials = Testimonial.objects.filter(is_active=True).all()
    for t in testimonials:
        t.photo_url = get_image_url(t, 'photo')
    
    ctx.update({
        'page': 'Accueil',
        'hero': hero,
        'about': about,
        'news': news,
        'publications': publications,
        'testimonials': testimonials,
    })
    return render(request, 'core/index.html', ctx)

def about(request):
    ctx = get_common_context()
    about = AboutSection.objects.first()
    gallery = AboutGalleryImage.objects.all().order_by('order')
    
    # Get image URL for about section
    if about:
        about.image_url = get_image_url(about, 'image')
    
    # Get image URLs for gallery
    for img in gallery:
        img.image_url = get_image_url(img, 'image')

    # Testimonials to display on about page
    testimonials = Testimonial.objects.filter(is_active=True).all()
    for t in testimonials:
        t.photo_url = get_image_url(t, 'photo')
    
    ctx.update({
        'page': 'À propos',
        'about': about,
        'gallery': gallery,
        'testimonials': testimonials,
    })
    return render(request, 'core/about.html', ctx)

def news(request):
    ctx = get_common_context()
    news_list = NewsItem.objects.all()
    for item in news_list:
        item.image_url = get_image_url(item, 'image')
    
    ctx.update({
        'page': 'Actualités',
        'news_list': news_list,
    })
    return render(request, 'core/news.html', ctx)

def members(request):
    ctx = get_common_context()
    members = Member.objects.filter(is_active=True).all()
    for m in members:
        m.photo_url = get_image_url(m, 'photo')
    
    ctx.update({
        'page': 'Membres',
        'members': members,
    })
    return render(request, 'core/members.html', ctx)

def publications(request):
    ctx = get_common_context()
    publications = Publication.objects.all()
    for item in publications:
        item.image_url = get_image_url(item, 'image')
    
    ctx.update({
        'page': 'Recherche & Publications',
        'publications': publications,
    })
    return render(request, 'core/publications.html', ctx)

def contact(request):
    ctx = get_common_context()
    ctx['page'] = 'Contact'
    ctx['form'] = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            pass
        ctx['form'] = form
    return render(request, 'core/contact.html', ctx)

def join(request):
    ctx = get_common_context()
    ctx['page'] = 'Devenir un membre'
    ctx['form'] = MembershipRequestForm()
    
    if request.method == 'POST':
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            # Create membership request
            MembershipRequest.objects.create(
                nom_complet=form.cleaned_data['nom_complet'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data.get('telephone', ''),
                profil=form.cleaned_data['profil'],
                organisation=form.cleaned_data.get('organisation', ''),
                domaine=form.cleaned_data['domaine'],
                niveau=form.cleaned_data.get('niveau', 'licence'),
                niveau_autre=form.cleaned_data.get('niveau_autre', ''),
                pays=form.cleaned_data.get('pays', 'senegal'),
                pays_autre=form.cleaned_data.get('pays_autre', ''),
                motivation=form.cleaned_data['motivation'],
            )
            ctx['success'] = True
            ctx['form'] = MembershipRequestForm()
        else:
            ctx['form'] = form
    
    return render(request, 'core/join.html', ctx)

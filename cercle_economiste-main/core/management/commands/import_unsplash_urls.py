from django.core.management.base import BaseCommand
import urllib.request
import imghdr

from core import models as cms


def fetch_image(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            try:
                ctype = resp.headers.get_content_type()
            except Exception:
                ctype = resp.getheader('Content-Type') if hasattr(resp, 'getheader') else None
            if not ctype or ctype == 'application/octet-stream':
                ext = imghdr.what(None, data) or 'jpeg'
                ctype = f'image/{ext if ext != "jpg" else "jpeg"}'
            return data, ctype
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return None, None


class Command(BaseCommand):
    help = 'Import Unsplash image URLs and assign to site models.'

    def handle(self, *args, **options):
        # Define precise URL mappings by section
        urls = {
            # Hero
            'hero': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1500&auto=format&fit=crop',
            # News (5 items)
            'news': [
                'https://images.unsplash.com/photo-1542744173-05336fcc7ad4?q=80&w=1200',  # Sommet de Dakar
                'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?q=80&w=1200',  # Croissance Verte
                'https://images.unsplash.com/photo-1591189863430-ab87e120f312?q=80&w=1200',  # Partenariat
                'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=1200',  # IA & Agriculture
                'https://images.unsplash.com/photo-1558494949-ef010cbdcc51?q=80&w=1200',   # Infrastructure Cloud
            ],
            # Publications (6 items)
            'publications': [
                'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=800',  # Rapport Annuel
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800',    # Policy Brief
                'https://images.unsplash.com/photo-1454165833767-027eeef1596e?auto=format&fit=crop&q=80&w=800',  # Étude Technique
                'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?auto=format&fit=crop&q=80&w=800',  # Working Paper
                'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200',  # Systèmes Fiscaux
                'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=800',  # Défaut (Bibliothèque)
            ],
            # About section (4 gallery items)
            'about_gallery': [
                'https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1600&auto=format&fit=crop',  # Hero Header
                'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1200&auto=format&fit=crop',  # Vision 2030
                'https://images.unsplash.com/photo-1454165833767-027eeef1596e?q=80&w=1200&auto=format&fit=crop',  # Rigueur Scientifique
                'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1200&auto=format&fit=crop',  # Panafricanisme
            ],
            # Members (4 items; override existing photo_blob)
            'members': [
                'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop',  # Dr. Amina Diallo
                'https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=800&auto=format&fit=crop',    # Prof. Samuel K. Moyo
                'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=800&auto=format&fit=crop',  # Mme. Hawa Cissé
                'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=800&auto=format&fit=crop',   # Jean-Marc Koffi
            ],
            # Testimonials (3 items)
            'testimonials': [
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',  # Prof. Temitope Okafor
                'https://images.unsplash.com/photo-1531384441138-2736e62e0919?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',  # Dr. Moussa Fofana
                'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',   # Sarah El-Mahdi
            ],
        }

        # Hero
        hero = cms.HeroSection.objects.first()
        if hero:
            data, mime = fetch_image(urls['hero'])
            if data:
                hero.image_blob = data
                hero.image_blob_mime = mime
                hero.save()
                self.stdout.write(f'✓ HeroSection updated ({len(data)} bytes)')

        # News (match to first 5 NewsItem by id)
        news_list = list(cms.NewsItem.objects.order_by('id')[:len(urls['news'])])
        for i, (obj, url) in enumerate(zip(news_list, urls['news'])):
            data, mime = fetch_image(url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
                obj.save()
                self.stdout.write(f'✓ NewsItem {obj.id} updated ({len(data)} bytes)')

        # Publications (match to first 6 Publication by id)
        pub_list = list(cms.Publication.objects.order_by('id')[:len(urls['publications'])])
        for i, (obj, url) in enumerate(zip(pub_list, urls['publications'])):
            data, mime = fetch_image(url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
                obj.save()
                self.stdout.write(f'✓ Publication {obj.id} updated ({len(data)} bytes)')

        # About Gallery (update first 4 items, rest remain unchanged)
        about_gal = list(cms.AboutGalleryImage.objects.order_by('order')[:len(urls['about_gallery'])])
        for i, (obj, url) in enumerate(zip(about_gal, urls['about_gallery'])):
            data, mime = fetch_image(url)
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
                obj.save()
                self.stdout.write(f'✓ AboutGalleryImage {obj.id} ({obj.title}) updated ({len(data)} bytes)')

        # Members (match to first 4 Member by id)
        member_list = list(cms.Member.objects.order_by('id')[:len(urls['members'])])
        for obj, url in zip(member_list, urls['members']):
            data, mime = fetch_image(url)
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
                obj.save()
                self.stdout.write(f'✓ Member {obj.id} ({obj.name}) updated ({len(data)} bytes)')

        # Testimonials (match to first 3 Testimonial by id)
        test_list = list(cms.Testimonial.objects.order_by('id')[:len(urls['testimonials'])])
        for obj, url in zip(test_list, urls['testimonials']):
            data, mime = fetch_image(url)
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
                obj.save()
                self.stdout.write(f'✓ Testimonial {obj.id} ({obj.author}) updated ({len(data)} bytes)')

        self.stdout.write('\n✓ All images imported from Unsplash URLs.')

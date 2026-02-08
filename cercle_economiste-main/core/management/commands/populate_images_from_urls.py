from django.core.management.base import BaseCommand
from core.models import *
import requests
import imghdr


class Command(BaseCommand):
    help = 'Populate image_blob fields from a predefined list of public image URLs'

    def handle(self, *args, **options):
        # Lists from user (order matters)
        hero_urls = [
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1500&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1600&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1557804506-669a67965ba0?q=80&w=1600',
        ]

        news_urls = [
            'https://images.unsplash.com/photo-1542744173-05336fcc7ad4?q=80&w=1200',
            'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?q=80&w=1200',
            'https://images.unsplash.com/photo-1591189863430-ab87e120f312?q=80&w=1200',
            'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=1200',
            'https://images.unsplash.com/photo-1558494949-ef010cbdcc51?q=80&w=1200',
        ]

        publication_urls = [
            'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1454165833767-027eeef1596e?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200',
            'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=800',
        ]

        about_urls = [
            'https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1600&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1200&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1454165833767-027eeef1596e?q=80&w=1200&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1200&auto=format&fit=crop',
        ]

        member_urls = [
            'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=800&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=800&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=800&auto=format&fit=crop',
        ]

        testimonial_urls = [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1531384441138-2736e62e0919?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80',
        ]

        gallery_urls = about_urls + publication_urls[:2]

        def fetch(url):
            try:
                r = requests.get(url, timeout=20)
                r.raise_for_status()
                data = r.content
                mime = r.headers.get('Content-Type')
                if not mime:
                    ext = imghdr.what(None, data) or 'jpeg'
                    mime = f'image/{ext if ext!='jpg' else "jpeg"}'
                return data, mime
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to fetch {url}: {e}'))
                return None, None

        # Hero
        hero = HeroSection.objects.first()
        if hero:
            data, mime = fetch(hero_urls[0])
            if data:
                hero.image_blob = data
                hero.image_blob_mime = mime
                hero.save()
                self.stdout.write(self.style.SUCCESS('Updated Hero image'))

        # About
        about = AboutSection.objects.first()
        if about:
            data, mime = fetch(about_urls[0])
            if data:
                about.image_blob = data
                about.image_blob_mime = mime
                about.save()
                self.stdout.write(self.style.SUCCESS('Updated About image'))

        # Gallery
        gallery = list(AboutGalleryImage.objects.all().order_by('order'))
        for i, img in enumerate(gallery):
            url = gallery_urls[i % len(gallery_urls)]
            data, mime = fetch(url)
            if data:
                img.image_blob = data
                img.image_blob_mime = mime
                img.save()
        if gallery:
            self.stdout.write(self.style.SUCCESS(f'Updated {len(gallery)} gallery images'))

        # News
        news = list(NewsItem.objects.all().order_by('created_at'))
        for i, item in enumerate(news):
            url = news_urls[i % len(news_urls)]
            data, mime = fetch(url)
            if data:
                item.image_blob = data
                item.image_blob_mime = mime
                item.save()
        if news:
            self.stdout.write(self.style.SUCCESS(f'Updated {len(news)} news images'))

        # Publications
        pubs = list(Publication.objects.all().order_by('created_at'))
        for i, item in enumerate(pubs):
            url = publication_urls[i % len(publication_urls)]
            data, mime = fetch(url)
            if data:
                item.image_blob = data
                item.image_blob_mime = mime
                item.save()
        if pubs:
            self.stdout.write(self.style.SUCCESS(f'Updated {len(pubs)} publication images'))

        # Members
        members = list(Member.objects.all().order_by('order','name'))
        for i, m in enumerate(members):
            url = member_urls[i % len(member_urls)]
            data, mime = fetch(url)
            if data:
                m.photo_blob = data
                m.photo_blob_mime = mime
                m.save()
        if members:
            self.stdout.write(self.style.SUCCESS(f'Updated {len(members)} member photos'))

        # Testimonials
        tests = list(Testimonial.objects.all().order_by('order'))
        for i, t in enumerate(tests):
            url = testimonial_urls[i % len(testimonial_urls)]
            data, mime = fetch(url)
            if data:
                t.photo_blob = data
                t.photo_blob_mime = mime
                t.save()
        if tests:
            self.stdout.write(self.style.SUCCESS(f'Updated {len(tests)} testimonial photos'))

        self.stdout.write(self.style.SUCCESS('Image population complete'))

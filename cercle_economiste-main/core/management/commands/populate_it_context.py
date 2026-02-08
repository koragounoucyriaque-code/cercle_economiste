from django.core.management.base import BaseCommand
from django.utils import timezone
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
    except Exception:
        return None, None


class Command(BaseCommand):
    help = 'Populate site models with IT-themed titles, descriptions and images; set About gallery to 6 items.'

    def handle(self, *args, **options):
        now = timezone.now().strftime('%Y-%m-%d')

        # Hero
        hero = cms.HeroSection.objects.first()
        if hero:
            hero.title = 'Solutions Informatiques Innovantes'
            hero.subtitle = 'Nous concevons des systèmes robustes pour l\'entreprise moderne.'
            data, mime = fetch_image(f'https://picsum.photos/seed/hero-it/1200/600')
            if data:
                hero.image_blob = data
                hero.image_blob_mime = mime
            hero.save()
            self.stdout.write('Updated HeroSection')

        # AboutSection
        about = cms.AboutSection.objects.first()
        if about:
            about.title = 'Qui sommes-nous ?'
            about.content = (
                "Nous sommes une équipe d'ingénieurs informatique spécialisée dans le développement "
                "de logiciels, l'architecture cloud et la cybersécurité. Nous aidons les organisations "
                "à transformer numériquement leurs processus et à garder leurs données sécurisées."
            )
            data, mime = fetch_image('https://picsum.photos/seed/about-it/800/400')
            if data:
                about.image_blob = data
                about.image_blob_mime = mime
            about.save()
            self.stdout.write('Updated AboutSection')

        # About gallery: ensure exactly 6 items with clear labels
        desired = [
            ('Mission', 'Notre mission : automatiser et sécuriser vos workflows.'),
            ('Vision', 'Être partenaire de confiance pour la transformation digitale.'),
            ('Services', 'Développement, cloud, data, sécurité et formation.'),
            ('Sécurité', 'Conception sécurisée; audits et conformité.'),
            ('Equipe', 'Ingénieurs et chercheurs dédiés.'),
            ('Contact', 'Contactez-nous pour une démo ou un audit technique.'),
        ]

        gallery = list(cms.AboutGalleryImage.objects.all().order_by('order') )
        # trim extras
        while len(gallery) > 6:
            obj = gallery.pop()
            obj.delete()
        # create missing
        for i, (title, desc) in enumerate(desired):
            if i < len(gallery):
                obj = gallery[i]
                obj.title = title
                obj.description = desc
            else:
                obj = cms.AboutGalleryImage(title=title, description=desc, order=i)
            data, mime = fetch_image(f'https://picsum.photos/seed/about-{i+1}-it/800/600')
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
            obj.order = i
            obj.save()
        self.stdout.write('Ensured 6 AboutGalleryImage items')

        # News items: set to IT news
        for i, obj in enumerate(cms.NewsItem.objects.all().order_by('id')):
            obj.title = f'Actualité informatique {i+1}'
            obj.content = f'Annonce technique et résumé pour l\'actualité {i+1}.'
            obj.category = 'Informatique'
            obj.date_str = now
            data, mime = fetch_image(f'https://picsum.photos/seed/news-it-{i+1}/800/450')
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
            obj.save()
        self.stdout.write('Updated NewsItem entries')

        # Publications
        for i, obj in enumerate(cms.Publication.objects.all().order_by('id')):
            obj.title = f'Publication technique {i+1}'
            obj.content = 'Étude technique et bonnes pratiques en informatique.'
            obj.category = 'research'
            obj.date_str = now
            data, mime = fetch_image(f'https://picsum.photos/seed/pub-it-{i+1}/800/450')
            if data:
                obj.image_blob = data
                obj.image_blob_mime = mime
            obj.save()
        self.stdout.write('Updated Publication entries')

        # Members
        for i, obj in enumerate(cms.Member.objects.all().order_by('order')):
            obj.name = obj.name or f'Ingénieur {i+1}'
            obj.position = obj.position or 'Ingénieur logiciel'
            obj.description = 'Spécialiste en développement logiciel et architecture.'
            data, mime = fetch_image(f'https://picsum.photos/seed/member-it-{i+1}/400/400')
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
            obj.save()
        self.stdout.write('Updated Member entries')

        # Testimonials
        for i, obj in enumerate(cms.Testimonial.objects.all().order_by('order')):
            obj.quote = obj.quote or 'Leur expertise technique a transformé notre produit.'
            obj.author = obj.author or f'Client {i+1}'
            obj.role = obj.role or 'CTO'
            data, mime = fetch_image(f'https://picsum.photos/seed/testimonial-it-{i+1}/400/400')
            if data:
                obj.photo_blob = data
                obj.photo_blob_mime = mime
            obj.save()
        self.stdout.write('Updated Testimonial entries')

        self.stdout.write('\nAll content updated to IT-themed texts and images.')

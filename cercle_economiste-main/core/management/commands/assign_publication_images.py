from django.core.management.base import BaseCommand
from core.models import Publication
import requests, imghdr


class Command(BaseCommand):
    help = 'Assign images to the three recently added publications'

    def handle(self, *args, **options):
        # Map publication title -> image URL
        mapping = {
            "Économie Inclusive en Afrique 2026": 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=800',
            "Transition Énergétique et Emplois": 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800',
            "Commerce Régional et Intégration": 'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?auto=format&fit=crop&q=80&w=800',
        }

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

        updated = 0
        for title, url in mapping.items():
            try:
                pub = Publication.objects.get(title=title)
            except Publication.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Publication not found: {title}'))
                continue
            if pub.image_blob:
                self.stdout.write(self.style.NOTICE(f'Publication already has image: {title}'))
                continue
            data, mime = fetch(url)
            if data:
                pub.image_blob = data
                pub.image_blob_mime = mime
                pub.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Assigned image for: {title}'))

        self.stdout.write(self.style.SUCCESS(f'Done — images assigned: {updated}'))

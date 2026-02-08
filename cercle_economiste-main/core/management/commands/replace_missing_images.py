from django.core.management.base import BaseCommand
from core.models import AboutGalleryImage, Publication
import requests
import imghdr


class Command(BaseCommand):
    help = 'Replace missing image blobs with fallback public URLs'

    def handle(self, *args, **options):
        fallback_urls = [
            'https://images.unsplash.com/photo-1508921912186-1d1a45ebb3c1?q=80&w=1200&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?q=80&w=1200&auto=format&fit=crop',
        ]

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
        idx = 0

        # About gallery images
        for img in AboutGalleryImage.objects.all():
            if not img.image_blob:
                url = fallback_urls[idx % len(fallback_urls)]
                data, mime = fetch(url)
                if data:
                    img.image_blob = data
                    img.image_blob_mime = mime
                    img.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated gallery image id={img.pk}'))
                idx += 1

        # Publications
        for pub in Publication.objects.all():
            if not pub.image_blob:
                url = fallback_urls[idx % len(fallback_urls)]
                data, mime = fetch(url)
                if data:
                    pub.image_blob = data
                    pub.image_blob_mime = mime
                    pub.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated publication id={pub.pk}'))
                idx += 1

        self.stdout.write(self.style.SUCCESS(f'Replace complete, total updated: {updated}'))

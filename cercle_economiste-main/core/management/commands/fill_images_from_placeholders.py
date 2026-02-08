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
    except Exception:
        return None, None


class Command(BaseCommand):
    help = 'Fill missing image BLOBs using placeholder image URLs.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Do not save changes')

    def handle(self, *args, **options):
        dry = options.get('dry_run', False)
        targets = [
            (cms.HeroSection, 'image_blob'),
            (cms.AboutSection, 'image_blob'),
            (cms.AboutGalleryImage, 'image_blob'),
            (cms.NewsItem, 'image_blob'),
            (cms.Publication, 'image_blob'),
            (cms.Member, 'photo_blob'),
            (cms.Testimonial, 'photo_blob'),
        ]

        summary = []
        for model, field in targets:
            qs = model.objects.all()
            to_fill = []
            for obj in qs:
                val = getattr(obj, field)
                if not val:
                    to_fill.append(obj)

            count = len(to_fill)
            self.stdout.write(f'Processing {model.__name__}: {count} missing')
            updated = 0
            for obj in to_fill:
                # build a stable placeholder URL
                url = f'https://picsum.photos/seed/{model.__name__.lower()}{obj.pk}/800/600'
                data, mime = fetch_image(url)
                if data:
                    if not dry:
                        setattr(obj, field, data)
                        # set mime field if present
                        mime_field = field + '_mime' if hasattr(obj, field + '_mime') else None
                        if mime_field and hasattr(obj, mime_field):
                            setattr(obj, mime_field, mime)
                        obj.save()
                    updated += 1
                    self.stdout.write(f'  filled {model.__name__} id={obj.pk} from {url} ({len(data)} bytes)')
                else:
                    # fallback to placeholder.com
                    url2 = f'https://via.placeholder.com/800x600?text={model.__name__}+{obj.pk}'
                    data2, mime2 = fetch_image(url2)
                    if data2:
                        if not dry:
                            setattr(obj, field, data2)
                            mime_field = field + '_mime' if hasattr(obj, field + '_mime') else None
                            if mime_field and hasattr(obj, mime_field):
                                setattr(obj, mime_field, mime2)
                            obj.save()
                        updated += 1
                        self.stdout.write(f'  filled {model.__name__} id={obj.pk} from {url2} ({len(data2)} bytes)')
                    else:
                        self.stdout.write(f'  failed to fetch for {model.__name__} id={obj.pk}')

            summary.append((model.__name__, count, updated))

        self.stdout.write('\nSummary:')
        for name, missing, done in summary:
            self.stdout.write(f' - {name}: missing={missing}, filled={done}')

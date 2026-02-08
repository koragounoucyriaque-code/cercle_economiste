from django.core.management.base import BaseCommand
from core.models import Publication


class Command(BaseCommand):
    help = 'Add three additional publications'

    def handle(self, *args, **options):
        pubs = [
            ("Économie Inclusive en Afrique 2026", 'report', 'Janvier 2026'),
            ("Transition Énergétique et Emplois", 'research', 'Décembre 2025'),
            ("Commerce Régional et Intégration", 'article', 'Novembre 2025'),
        ]
        created = 0
        for title, category, date_str in pubs:
            obj, was_created = Publication.objects.update_or_create(
                title=title,
                defaults={'category': category, 'date_str': date_str}
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created publication: {title}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Updated publication: {title}'))

        self.stdout.write(self.style.SUCCESS(f'Done — publications processed: {len(pubs)}, new: {created}'))

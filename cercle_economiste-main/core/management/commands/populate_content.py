from django.core.management.base import BaseCommand
from core.models import GlobalSettings, HeroSection, AboutSection, AboutGalleryImage, NewsItem, Publication, Member, Testimonial


class Command(BaseCommand):
    help = 'Create or update initial site content according to provided inventory'

    def handle(self, *args, **options):
        # Global settings
        gs = GlobalSettings.objects.first()
        if not gs:
            gs = GlobalSettings.objects.create()
        gs.email_contact = 'contact@ecoafrique.org'
        gs.phone = '+221 33 800 00 00'
        gs.address = 'Dakar, Sénégal'
        gs.save()
        self.stdout.write(self.style.SUCCESS('GlobalSettings updated'))

        # Hero
        hero = HeroSection.objects.first()
        if not hero:
            hero = HeroSection.objects.create(title='Façonner l\'avenir Économique de l\'Afrique', subtitle="L'Expertise Économique au Service du Continent")
        else:
            hero.title = "Façonner l'avenir Économique de l'Afrique"
            hero.subtitle = "L'Expertise Économique au Service du Continent"
            hero.save()
        self.stdout.write(self.style.SUCCESS('HeroSection updated'))

        # About
        about = AboutSection.objects.first()
        about_content = (
            "L'Association des Économistes de l'Afrique (AEA) est une organisation panafricaine dédiée "
            "à la promotion de la recherche économique souveraine et au renforcement des capacités pour un développement inclusif."
        )
        if not about:
            about = AboutSection.objects.create(title='Qui sommes-nous ?', content=about_content)
        else:
            about.title = 'Qui sommes-nous ?'
            about.content = about_content
            about.save()
        self.stdout.write(self.style.SUCCESS('AboutSection updated'))

        # About gallery
        gallery_items = [
            ('Vision 2030', 'Influencer les politiques publiques par une expertise locale.', 1),
            ('Rigueur Scientifique', 'Des méthodologies basées sur l\'évidence et les données réelles.', 2),
            ('Panafricanisme', 'Un réseau interconnecté à travers les 54 nations du continent.', 3),
        ]
        for title, desc, order in gallery_items:
            obj, created = AboutGalleryImage.objects.update_or_create(title=title, defaults={'description': desc, 'order': order})
        self.stdout.write(self.style.SUCCESS('AboutGalleryImage items updated'))

        # News
        news_list = [
            ("Souveraineté Monétaire : Sommet de Dakar", 'CONFÉRENCE', '15 JAN 2026'),
            ("Croissance Verte : L\'hydrogène au Sahel", 'RAPPORT', '12 JAN 2026'),
            ("Partenariat AEA-BCEAO", 'PARTENARIAT', '08 JAN 2026'),
            ("IA & Agriculture : Opportunités", 'TECH', '05 JAN 2026'),
        ]
        for title, category, date_str in news_list:
            NewsItem.objects.update_or_create(title=title, defaults={'category': category, 'date_str': date_str})
        self.stdout.write(self.style.SUCCESS('NewsItem entries updated'))

        # Publications
        pubs = [
            ("PERSPECTIVES ÉCONOMIQUES 2025", 'report', 'Mars 2025'),
            ("LA DIGITALISATION DE LA FINANCE", 'research', 'Février 2025'),
            ("HARMONISATION MONÉTAIRE", 'article', 'Janvier 2025'),
        ]
        for title, category, date_str in pubs:
            Publication.objects.update_or_create(title=title, defaults={'category': category, 'date_str': date_str})
        self.stdout.write(self.style.SUCCESS('Publication entries updated'))

        # Members
        members = [
            ("Dr. Amina Diallo", 'Présidente', 'president'),
            ("Mme. Hawa Cissé", 'Vice-Présidente', 'vice_president'),
            ("Prof. Samuel K. Moyo", 'Directeur Scientifique', 'researcher'),
            ("Jean-Marc Koffi", 'Analyste Senior', 'member'),
        ]
        for name, position, role in members:
            Member.objects.update_or_create(name=name, defaults={'position': position, 'role': role})
        self.stdout.write(self.style.SUCCESS('Member entries updated'))

        # Testimonials
        testimonials = [
            ("L'AEA est le pivot central de la réflexion stratégique.", 'Prof. Temitope Okafor', 'Doyen'),
            ("Capacité exceptionnelle de transformation de données.", 'Dr. Moussa Fofana', 'Conseiller'),
        ]
        for quote, author, role in testimonials:
            Testimonial.objects.update_or_create(author=author, defaults={'quote': quote, 'role': role})
        self.stdout.write(self.style.SUCCESS('Testimonial entries updated'))

        self.stdout.write(self.style.SUCCESS('Content population complete'))

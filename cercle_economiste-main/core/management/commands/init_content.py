
from django.core.management.base import BaseCommand
from core.models import *

class Command(BaseCommand):
    help = 'Initialise les données'

    def handle(self, *args, **kwargs):
        if not GlobalSettings.objects.exists(): GlobalSettings.objects.create()

        if not HeroSection.objects.exists():
            HeroSection.objects.create(title="Façonner l'avenir Économique de l'Afrique", subtitle="L'Expertise Économique au Service du Continent", image_url="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80")

        if not AboutSection.objects.exists():
            AboutSection.objects.create(content="L'Association des Économistes de l'Afrique (AEA) est une organisation panafricaine dédiée à la promotion de la recherche économique...")

        if NewsItem.objects.count() == 0:
            NewsItem.objects.create(title="Partenariat Stratégique UA", date_str="1 JAN 2026", category="Partenariat", image_url="https://images.unsplash.com/photo-1577962917302-cd874c4e31d2?w=800")
            NewsItem.objects.create(title="Politiques Économiques", date_str="5 JAN 2026", category="Événement", image_url="https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800")
            NewsItem.objects.create(title="Rapport Développement", date_str="10 JAN 2026", category="Publication", image_url="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800")
            NewsItem.objects.create(title="Conférence Panafricaine", date_str="15 JAN 2026", category="Conférence", image_url="https://images.unsplash.com/photo-1544531320-dadbed4d130e?w=800")

        if Publication.objects.count() == 0:
            Publication.objects.create(title="Impact ZLECAf", date_str="15 FEV 2025", category="Étude", image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800")
            Publication.objects.create(title="Politique Monétaire", date_str="20 FEV 2025", category="Policy Brief", image_url="https://images.unsplash.com/photo-1611974765270-ca1258634369?w=800")
            Publication.objects.create(title="Digitalisation Finance", date_str="28 FEV 2025", category="Rapport", image_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800")
            Publication.objects.create(title="Agriculture Durable", date_str="10 MAR 2025", category="Recherche", image_url="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800")

        if Testimonial.objects.count() == 0:
            Testimonial.objects.create(quote="Les ressources de l'AEA sont inestimables.", author="Prof. Temitope Okafor", role="Université de Lagos", photo_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150")
            Testimonial.objects.create(quote="Une plateforme essentielle.", author="Dr. Sarah Mbeki", role="Ministère Finances, RSA", photo_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150")
            Testimonial.objects.create(quote="Crucial pour la prochaine génération.", author="Jean-Claude Kouassi", role="BAD", photo_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150")
            
        if Member.objects.count() == 0:
             Member.objects.create(name="Dr. Amina Diallo", position="Présidente", photo_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400", description="Experte Macro", order=1, linkedin="#")
             Member.objects.create(name="Prof. Samuel K. Moyo", position="Directeur", photo_url="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400", description="Spécialiste Dev", order=2, twitter="#")

        self.stdout.write(self.style.SUCCESS('Données chargées pour association_cabro !'))


from django.db import models
from django.core.validators import URLValidator

class GlobalSettings(models.Model):
    email_contact = models.EmailField(default="contact@ecoafrique.org")
    phone = models.CharField(max_length=50, default="+221 33 800 00 00")
    address = models.CharField(max_length=200, default="Dakar, Sénégal")
    
    class Meta:
        verbose_name_plural = "Global Settings"
    
    def __str__(self):
        return "Site Settings"


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image_blob = models.BinaryField(blank=True, null=True)
    image_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Hero Sections"


class AboutSection(models.Model):
    title = models.CharField(max_length=200, default="Qui sommes-nous ?")
    content = models.TextField()
    image_blob = models.BinaryField(blank=True, null=True)
    image_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "About Sections"


class AboutGalleryImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_blob = models.BinaryField(blank=True, null=True)
    image_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "About Gallery Images"


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    date_str = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    image_blob = models.BinaryField(blank=True, null=True)
    image_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "News Items"


class Publication(models.Model):
    CATEGORY_CHOICES = [
        ('research', 'Recherche'),
        ('report', 'Rapport'),
        ('article', 'Article'),
        ('other', 'Autre'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    date_str = models.CharField(max_length=50)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='research')
    image_blob = models.BinaryField(blank=True, null=True)
    image_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Publications"


class Member(models.Model):
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('vice_president', 'Vice-Président'),
        ('secretary', 'Secrétaire'),
        ('treasurer', 'Trésorier'),
        ('member', 'Membre'),
        ('researcher', 'Chercheur'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member')
    description = models.TextField(blank=True)
    photo_blob = models.BinaryField(blank=True, null=True)
    photo_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Members"


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo_blob = models.BinaryField(blank=True, null=True)
    photo_blob_mime = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Témoignage de {self.author}"
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Testimonials"


class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
    ]
    
    nom_complet = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    profil = models.CharField(max_length=100, help_text='Ex: Chercheur, Étudiant, Professionnel')
    organisation = models.CharField(max_length=100, blank=True)
    domaine = models.CharField(max_length=100, help_text='Votre domaine d\'expertise')
    # Niveau d'études
    NIVEAU_CHOICES = [
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='licence')
    niveau_autre = models.CharField(max_length=100, blank=True)
    # Pays
    PAYS_CHOICES = [
        ('afghanistan', 'Afghanistan'),
        ('albania', 'Albania'),
        ('algeria', 'Algérie'),
        ('andorra', 'Andorra'),
        ('angola', 'Angola'),
        ('antigua_and_barbuda', 'Antigua and Barbuda'),
        ('argentina', 'Argentina'),
        ('armenia', 'Armenia'),
        ('australia', 'Australia'),
        ('austria', 'Austria'),
        ('azerbaijan', 'Azerbaijan'),
        ('bahamas', 'Bahamas'),
        ('bahrain', 'Bahrain'),
        ('bangladesh', 'Bangladesh'),
        ('barbados', 'Barbados'),
        ('belarus', 'Belarus'),
        ('belgium', 'Belgium'),
        ('belize', 'Belize'),
        ('benin', 'Bénin'),
        ('bhutan', 'Bhutan'),
        ('bolivia', 'Bolivia'),
        ('bosnia_and_herzegovina', 'Bosnia and Herzegovina'),
        ('botswana', 'Botswana'),
        ('brazil', 'Brazil'),
        ('brunei', 'Brunei Darussalam'),
        ('bulgaria', 'Bulgaria'),
        ('burkina_faso', 'Burkina Faso'),
        ('burundi', 'Burundi'),
        ('cabo_verde', 'Cabo Verde'),
        ('cambodia', 'Cambodia'),
        ('cameroon', 'Cameroun'),
        ('canada', 'Canada'),
        ('central_african_republic', 'Central African Republic'),
        ('chad', 'Chad'),
        ('chile', 'Chile'),
        ('china', 'China'),
        ('colombia', 'Colombia'),
        ('comoros', 'Comoros'),
        ('congo', 'Congo'),
        ('democratic_republic_of_congo', 'Congo (Democratic Republic)'),
        ('costa_rica', 'Costa Rica'),
        ('cote_divoire', 'Côte d\'Ivoire'),
        ('croatia', 'Croatia'),
        ('cuba', 'Cuba'),
        ('cyprus', 'Cyprus'),
        ('czech_republic', 'Czech Republic'),
        ('denmark', 'Denmark'),
        ('djibouti', 'Djibouti'),
        ('dominica', 'Dominica'),
        ('dominican_republic', 'Dominican Republic'),
        ('ecuador', 'Ecuador'),
        ('egypt', 'Egypt'),
        ('el_salvador', 'El Salvador'),
        ('equatorial_guinea', 'Equatorial Guinea'),
        ('eritrea', 'Eritrea'),
        ('estonia', 'Estonia'),
        ('eswatini', 'Eswatini'),
        ('ethiopia', 'Ethiopia'),
        ('fiji', 'Fiji'),
        ('finland', 'Finland'),
        ('france', 'France'),
        ('gabon', 'Gabon'),
        ('gambia', 'Gambia'),
        ('georgia', 'Georgia'),
        ('germany', 'Germany'),
        ('ghana', 'Ghana'),
        ('greece', 'Greece'),
        ('grenada', 'Grenada'),
        ('guatemala', 'Guatemala'),
        ('guinea', 'Guinea'),
        ('guinea_bissau', 'Guinea-Bissau'),
        ('guyana', 'Guyana'),
        ('haiti', 'Haiti'),
        ('honduras', 'Honduras'),
        ('hungary', 'Hungary'),
        ('iceland', 'Iceland'),
        ('india', 'India'),
        ('indonesia', 'Indonesia'),
        ('iran', 'Iran'),
        ('iraq', 'Iraq'),
        ('ireland', 'Ireland'),
        ('israel', 'Israel'),
        ('italy', 'Italy'),
        ('jamaica', 'Jamaica'),
        ('japan', 'Japan'),
        ('jordan', 'Jordan'),
        ('kazakhstan', 'Kazakhstan'),
        ('kenya', 'Kenya'),
        ('kiribati', 'Kiribati'),
        ('kuwait', 'Kuwait'),
        ('kyrgyzstan', 'Kyrgyzstan'),
        ('laos', 'Lao People\'s Democratic Republic'),
        ('latvia', 'Latvia'),
        ('lebanon', 'Lebanon'),
        ('lesotho', 'Lesotho'),
        ('liberia', 'Liberia'),
        ('libya', 'Libya'),
        ('liechtenstein', 'Liechtenstein'),
        ('lithuania', 'Lithuania'),
        ('luxembourg', 'Luxembourg'),
        ('madagascar', 'Madagascar'),
        ('malawi', 'Malawi'),
        ('malaysia', 'Malaysia'),
        ('maldives', 'Maldives'),
        ('mali', 'Mali'),
        ('malta', 'Malta'),
        ('marshall_islands', 'Marshall Islands'),
        ('mauritania', 'Mauritania'),
        ('mauritius', 'Mauritius'),
        ('mexico', 'Mexico'),
        ('micronesia', 'Micronesia'),
        ('moldova', 'Moldova'),
        ('monaco', 'Monaco'),
        ('mongolia', 'Mongolia'),
        ('montenegro', 'Montenegro'),
        ('morocco', 'Morocco'),
        ('mozambique', 'Mozambique'),
        ('myanmar', 'Myanmar'),
        ('namibia', 'Namibia'),
        ('nauru', 'Nauru'),
        ('nepal', 'Nepal'),
        ('netherlands', 'Netherlands'),
        ('new_zealand', 'New Zealand'),
        ('nicaragua', 'Nicaragua'),
        ('niger', 'Niger'),
        ('nigeria', 'Nigeria'),
        ('north_macedonia', 'North Macedonia'),
        ('norway', 'Norway'),
        ('oman', 'Oman'),
        ('pakistan', 'Pakistan'),
        ('palau', 'Palau'),
        ('panama', 'Panama'),
        ('papua_new_guinea', 'Papua New Guinea'),
        ('paraguay', 'Paraguay'),
        ('peru', 'Peru'),
        ('philippines', 'Philippines'),
        ('poland', 'Poland'),
        ('portugal', 'Portugal'),
        ('qatar', 'Qatar'),
        ('romania', 'Romania'),
        ('russia', 'Russia'),
        ('rwanda', 'Rwanda'),
        ('saint_kitts_and_nevis', 'Saint Kitts and Nevis'),
        ('saint_lucia', 'Saint Lucia'),
        ('saint_vincent_and_the_grenadines', 'Saint Vincent and the Grenadines'),
        ('samoa', 'Samoa'),
        ('san_marino', 'San Marino'),
        ('sao_tome_and_principe', 'Sao Tome and Principe'),
        ('saudi_arabia', 'Saudi Arabia'),
        ('senegal', 'Sénégal'),
        ('serbia', 'Serbia'),
        ('seychelles', 'Seychelles'),
        ('sierra_leone', 'Sierra Leone'),
        ('singapore', 'Singapore'),
        ('slovakia', 'Slovakia'),
        ('slovenia', 'Slovenia'),
        ('solomon_islands', 'Solomon Islands'),
        ('somalia', 'Somalia'),
        ('south_africa', 'South Africa'),
        ('south_sudan', 'South Sudan'),
        ('spain', 'Spain'),
        ('sri_lanka', 'Sri Lanka'),
        ('sudan', 'Sudan'),
        ('suriname', 'Suriname'),
        ('sweden', 'Sweden'),
        ('switzerland', 'Switzerland'),
        ('syria', 'Syrian Arab Republic'),
        ('taiwan', 'Taiwan'),
        ('tajikistan', 'Tajikistan'),
        ('tanzania', 'Tanzania'),
        ('thailand', 'Thailand'),
        ('timor_leste', 'Timor-Leste'),
        ('togo', 'Togo'),
        ('tonga', 'Tonga'),
        ('trinidad_and_tobago', 'Trinidad and Tobago'),
        ('tunisia', 'Tunisie'),
        ('turkey', 'Turkey'),
        ('turkmenistan', 'Turkmenistan'),
        ('tuvalu', 'Tuvalu'),
        ('uganda', 'Ouganda'),
        ('ukraine', 'Ukraine'),
        ('united_arab_emirates', 'United Arab Emirates'),
        ('united_kingdom', 'United Kingdom'),
        ('united_states', 'United States'),
        ('uruguay', 'Uruguay'),
        ('uzbekistan', 'Uzbekistan'),
        ('vanuatu', 'Vanuatu'),
        ('venezuela', 'Venezuela'),
        ('vietnam', 'Vietnam'),
        ('yemen', 'Yemen'),
        ('zambia', 'Zambia'),
        ('zimbabwe', 'Zimbabwe'),
        ('autre', 'Autre'),
    ]
    pays = models.CharField(max_length=50, choices=PAYS_CHOICES, default='benin')
    pays_autre = models.CharField(max_length=100, blank=True)
    motivation = models.TextField(help_text='Pourquoi souhaitez-vous rejoindre l\'association?')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Demande de {self.nom_complet} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Membership Requests"

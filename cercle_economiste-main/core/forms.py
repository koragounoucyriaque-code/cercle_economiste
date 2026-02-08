from django import forms


def make_admin_image_url_form(model):
    """Return a ModelForm subclass for `model` that adds optional
    file upload and URL fields for images/photos. The resulting form
    includes the model's fields plus these helper fields:
      - image_file, image_url_input
      - photo_file, photo_url_input
    Admins can use whichever is convenient (local file or URL).
    """

    class AdminImageURLForm(forms.ModelForm):
        image_file = forms.FileField(required=False, label='Upload image (local)')
        image_url_input = forms.CharField(required=False, label='Image URL',
                                          help_text='Paste an image URL to fetch into DB')

        photo_file = forms.FileField(required=False, label='Upload photo (local)')
        photo_url_input = forms.CharField(required=False, label='Photo URL',
                                         help_text='Paste a photo URL to fetch into DB')

        class Meta:
            fields = '__all__'

    # assign model to Meta after class creation to avoid NameError
    AdminImageURLForm.Meta.model = model
    return AdminImageURLForm

from django import forms
class ContactForm(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded text-sm focus:border-[#c25e3d] focus:bg-white outline-none', 'placeholder': 'Votre nom'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded text-sm focus:border-[#c25e3d] focus:bg-white outline-none', 'placeholder': 'Votre email'}))
    sujet = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded text-sm focus:border-[#c25e3d] focus:bg-white outline-none', 'placeholder': 'Sujet'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded text-sm focus:border-[#c25e3d] focus:bg-white outline-none', 'rows': 5, 'placeholder': 'Message...'}))


class MembershipRequestForm(forms.Form):
    input_class = 'w-full p-3 bg-gray-50 border border-gray-200 rounded text-sm focus:border-[#c25e3d] focus:bg-white outline-none'
    
    nom_complet = forms.CharField(
        max_length=100,
        label='Nom complet',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Votre nom complet'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': input_class, 'placeholder': 'Votre email'})
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        label='Téléphone',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Votre numéro de téléphone'})
    )
    profil = forms.CharField(
        max_length=100,
        label='Profil',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Ex: Chercheur, Étudiant, Professionnel'})
    )
    organisation = forms.CharField(
        max_length=100,
        required=False,
        label='Organisation/Entreprise',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Votre organisation (optionnel)'})
    )
    domaine = forms.CharField(
        max_length=100,
        label='Domaine d\'expertise',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Ex: Environnement, Énergie, etc.'})
    )
    # Niveau d'études
    NIVEAU_CHOICES = [
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]
    niveau = forms.ChoiceField(
        choices=NIVEAU_CHOICES,
        label='Niveau d\'études',
        widget=forms.Select(attrs={'class': input_class})
    )
    niveau_autre = forms.CharField(
        max_length=100,
        required=False,
        label='Précisez (niveau)',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Précisez si autre (ex: BTS, DUT, etc.)'})
    )
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
    pays = forms.ChoiceField(
        choices=PAYS_CHOICES,
        label='Pays',
        initial='benin',
        widget=forms.Select(attrs={'class': input_class})
    )
    pays_autre = forms.CharField(
        max_length=100,
        required=False,
        label='Précisez (pays)',
        widget=forms.TextInput(attrs={'class': input_class, 'placeholder': 'Précisez le pays si Autre'})
    )

    motivation = forms.CharField(
        label='Motivation',
        widget=forms.Textarea(attrs={'class': input_class, 'rows': 5, 'placeholder': 'Pourquoi souhaitez-vous rejoindre l\'association?'})
    )

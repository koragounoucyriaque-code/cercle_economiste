from django.conf import settings


def site_settings(request):
    return {
        'settings': {
            'email_contact': 'contact@aea.org',
            'phone': '+221 77 000 0000',
            'address': '123 Rue Exemple, Dakar, Sénégal',
            'social': {
                'twitter': 'https://twitter.com/',
                'facebook': 'https://facebook.com/',
                'linkedin': 'https://linkedin.com/',
            }
        }
    }

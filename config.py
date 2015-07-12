from authomatic.providers import oauth2


OAUTH_CONFIG = {
    'fb': {
        'class_': oauth2.Facebook,
        'consumer_key': '332553410258929',
        'consumer_secret': '************************',
        'scope': ['user_about_me', 'email'],
    },
}

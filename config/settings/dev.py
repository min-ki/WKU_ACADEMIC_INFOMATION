from .base import *

DEBUG = True
# debug toolbar
INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wku_webcrawler',
        'USER': 'min_2271',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

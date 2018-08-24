from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'deploy',
        'USER': 'wgp',
        'PASSWORD': 'wgp12345678',
        'HOST': 'wgp-deploy.crlzxdgbsegw.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

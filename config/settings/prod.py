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

# Raven Setting

GIT_ROOT = ROOT_DIR
if os.path.exists(os.path.join(GIT_ROOT, '.git')):
    release = raven.fetch_git_sha(GIT_ROOT)
else:
    release = 'dev'

RAVEN_CONFIG = {
    'dsn': 'https://f2c7021d0a614494995b485eae80850f:b5e97015d7e747de9e5c7d70cbc65375@sentry.io/1271429',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': release,
}

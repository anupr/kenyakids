# Django settings for helpline project.
import os
from django.utils.translation import ugettext_lazy as _

gettext_noop = lambda s: s
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

LANGUAGES = (
    ('en', gettext_noop('English')),
    ('fi', gettext_noop('Finnish')),
    ('sk', gettext_noop('Slovak')),
    ('ma', gettext_noop('Marathi')),
    ('hi', gettext_noop('Hindi')),
    ('ta', gettext_noop('Tamil')),
  )
  
MODELTRANSLATION_TRANSLATION_REGISTRY = "kenyakids.translation"
	
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kenyakids',
        'USER': 'lawgon',
        'PASSWORD': 'xxx',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Africa/Nairobi'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'smedia')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = 'http:kenfakids.web/smedia/'

STATIC_ROOT = '/home/lawgon/mvdp/staticfiles/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://kenyakids.web/staticfiles/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'aqq+*+1p7g^2i7#x)e0(l(3kn_yc@(e!-aqp2=hk_@l5^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'web.context_processors.settings_context_processor',
)
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'sorl.thumbnail',
    'south',
    'web',
    'modeltranslation',
    'rosetta',
)

LOGIN_URL = "/login/"
TMP_DIR = "/home/mvdpkummit/tmp/"
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "d/m/Y H:M:S"

PROJECT_NAME = _(u"Maharashtra Village Development Project")
SHORT_PROJECT_NAME = _(u"kenyakids")

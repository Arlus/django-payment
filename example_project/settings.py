# flake8: noqa

import os
import sys


def abspath(*args):
    return os.path.abspath(os.path.join(*args))


PROJECT_ROOT = abspath(os.path.dirname(__file__))
PAYMENT_MODULE_PATH = abspath(PROJECT_ROOT, '..')
sys.path.insert(0, PAYMENT_MODULE_PATH)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    },
}

SECRET_KEY = 'not_so_secret'

USE_TZ = True

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'djmoney',
    'tests',
    'payment.apps.PaymentConfig',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'project/static')]

MEDIA_URL = '/media/'

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Enable specific currencies (djmoney)
CURRENCIES = ['USD', 'EUR', 'JPY', 'GBP', 'CAD', 'CHF']


DUMMY = "dummy"
STRIPE = "stripe"
PAYBOX = "paybox"


CHECKOUT_PAYMENT_GATEWAYS = {
    DUMMY: "Dummy gateway",
    STRIPE: "Stripe",
    PAYBOX: "paybox"
}

PAYMENT_GATEWAYS = {
    DUMMY: {
        "module": "payment.gateways.dummy",
        "config": {
            "auto_capture": True,
            "connection_params": {},
            "template_path": "payment/dummy.html",
        },
    },
    STRIPE: {
        "module": "payment.gateways.stripe",
        "config": {
            "auto_capture": True,
            "template_path": "payment/stripe.html",
            "connection_params": {
                "public_key": os.environ.get("STRIPE_PUBLIC_KEY"),
                "secret_key": os.environ.get("STRIPE_SECRET_KEY"),
                "store_name": os.environ.get("STRIPE_STORE_NAME", "skioo shop"),
                "store_image": os.environ.get("STRIPE_STORE_IMAGE", None),
                "prefill": os.environ.get("STRIPE_PREFILL", True),
                "remember_me": os.environ.get("STRIPE_REMEMBER_ME", False),
                "locale": os.environ.get("STRIPE_LOCALE", "auto"),
                "enable_billing_address": os.environ.get(
                    "STRIPE_ENABLE_BILLING_ADDRESS", False
                ),
                "enable_shipping_address": os.environ.get(
                    "STRIPE_ENABLE_SHIPPING_ADDRESS", False
                ),
            },
        },
    },
    PAYBOX: {
        "module": "payment.gateways.paybox",
        "config": {
            "auto_capture": True,
            "template_path": "payment/paybox.html",
            "connection_params": {
                "public_key": os.environ.get("PAYBOX_PUBLIC_KEY") or "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF",
                "site": os.environ.get("PAYBOX_SITE") or "1999888",
                "rang": os.environ.get("PAYBOX_RANG") or "32",
                "identifiant": os.environ.get("PAYBOX_IDENTIFIANT") or "2",
                "production": False,
                "transaction_confirmation_url": os.environ.get("PAYBOX_TRANSACTION_CONFIRMATION_URL") or "http://xyz.xyn",
                "transaction_valid_url": os.environ.get("PAYBOX_TRANSACTION_VALIDATION_URL") or "http://xyz.xyn",
                "transaction_rejection_url": os.environ.get("PAYBOX_TRANSACTION_REJECTION_URL") or "http://xyz.xyn",
                "transaction_cancel_url": os.environ.get("PAYBOX_TRANSACTION_CANCEL_URL") or "http://xyz.xyn",
                "ipn_url": os.environ.get("PAYBOX_IPN_URL") or "http://xyz.xyn",
                "language": "GBR"

            },
        },
    }
}


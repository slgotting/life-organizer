import os

class Config:
    SECRET_KEY = 'hella-secret'

    SERVER_URI = 'http://127.0.0.1:5005' # this apps URI
    CLIENT_URI = 'http://127.0.0.1:5173'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailersend.net')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_TLS', True)
    MAIL_DEFAULT_SENDER = ("schedulr", "slgotting@gmail.com")
    # MAIL_DISPLAY_NAME = os.environ.get('MAIL_DISPLAY_NAME', 'SimplyMemorize')
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'MS_ag25EM@slgotting.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'slgotting')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'bN9V7XUgDH4Sxs82')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'qhqvemqlpxkulehy')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'sednlkaekdfigxcw')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'lnbwkqqepmckvxhm')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'fmqvvijflmrehblr')

    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/pw-api'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/steven/life-organizer-api/api/dev.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_OAUTH_CLIENT_IDS = {
        "web": "457555139413-rls7pj1ectoitbst0ufh9p7hhgnldai5.apps.googleusercontent.com",
        "android": "",
        "ios": "",
    }
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    # STRIPE STUFF # |UPDATE_ME|
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51PZtwRBIjE5s9OuT3Cpv7S0DUwYgWA3Cd3PVIUDqLxmc1ysrzqocp4F0yMerXyeoGzLL1fdfD5zlCPJ1SH8Sm5p100OivlEplB')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_2fa54cb20ff0115cd699eeb45a2dbd9a83d6ce9277b37ba30118866fb02a9ee8')

    STRIPE_PRODUCT_PLAN_MAP = {
        "prod_Qls8ShNOBEijlg": "Apprentice", # |UPDATE_ME|
        "prod_Qls8nCz5hv6HWV": "Cultivating", # |UPDATE_ME|
        "prod_Qls8DntduGIoM1": "Learned", # |UPDATE_ME|
        "prod_Qls9NvOUUVPKlu": "Lifetime", # |UPDATE_ME|
    }
    STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP = {
        'Free': {
            'monthly': None,
            'yearly': None,
        },
        'Apprentice': {
            'monthly': 'price_1PuKNtBIjE5s9OuTbFIKOJEO', # |UPDATE_ME|
            'yearly': None,
        },
        'Cultivating': {
            'monthly': 'price_1PuKODBIjE5s9OuTzwdWlQrc',
            'yearly': None,
        },
        'Learned': {
            'monthly': 'price_1PuKOTBIjE5s9OuTUYy4xXfg',
            'yearly': None,
        },
        'Lifetime': {
            'monthly': 'price_1PuKOiBIjE5s9OuT49tSwbhr',
            'yearly': 'price_1PuKOiBIjE5s9OuT49tSwbhr',
            'one_time': 'price_1PuKOiBIjE5s9OuT49tSwbhr',
        },
    }
    # STRIPE STUFF

    OPENAI_API_KEY = "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"

    MONGODB_SETTINGS = {
        "db": "life-organizer-dev",
        "host": "mongodb://127.0.0.1:27017/life-organizer-dev"
    }

class DockerDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////app/dev.db'
    SERVER_URI = 'http://127.0.0.1:5000' # this apps URI
    CLIENT_URI = 'http://127.0.0.1:5173'
    MONGODB_SETTINGS = {
        "db": "life-organizer-dev",
        "host": "mongodb://mongo:27017/life-organizer-dev"
    }

class LANDockerDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////app/dev.db'
    SERVER_URI = 'http://127.0.0.1:5000' # this apps URI
    CLIENT_URI = 'http://127.0.0.1:5173' # frontend URI
    MONGODB_SETTINGS = {
        "db": "life-organizer-dev",
        "host": "mongodb://127.0.0.1:27019/life-organizer-dev"
    }

class DevelopmentConfig(Config):
    pass

class StagingConfig(Config):
    SECRET_KEY = 'stagalaging-secret'

    SERVER_URI = 'https://staging.api.schedulr.ai' # this apps URI
    CLIENT_URI = 'https://staging.schedulr.ai'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/life-organizer-staging'
    MONGODB_SETTINGS = {
        "db": "life-organizer-staging",
        "host": "mongodb://127.0.0.1:27017/life-organizer-staging"
    }

class ProductionConfig(Config):

    SERVER_URI = 'https://api.schedulr.ai' # this apps URI
    CLIENT_URI = 'https://schedulr.ai'

    SECRET_KEY = 'q09j0f9j25gi9aw9rjfq29j3riojoiawbu9h40923ij323'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/life-organizer'
    MONGODB_SETTINGS = {
        "db": "life-organizer-prod",
        "host": "mongodb://127.0.0.1:27017/life-organizer-prod"
    }

    # STRIPE STUFF
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51PZtwRBIjE5s9OuT3Cpv7S0DUwYgWA3Cd3PVIUDqLxmc1ysrzqocp4F0yMerXyeoGzLL1fdfD5zlCPJ1SH8Sm5p100OivlEplB')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_nAhvHeZpKvWPDiGy7leRR9p7r6SoaeNH')

    STRIPE_PRODUCT_PLAN_MAP = {
        "prod_QlsAeSyaUb3kRf": "Apprentice", # |UPDATE_ME|
        "prod_QlsA8KiiEeRwPI": "Cultivating", # |UPDATE_ME|
        "prod_QlsAMTonEV3b8M": "Learned", # |UPDATE_ME|
        "prod_QlsAxlQkMAg4Vq": "Lifetime", # |UPDATE_ME|
    }
    STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP = {
        'Free': {
            'monthly': None,
            'yearly': None,
        },
        'Apprentice': {
            'monthly': 'price_1PuKQWBIjE5s9OuTm0Adg7Mw', # |UPDATE_ME|
            'yearly': None,
        },
        'Cultivating': {
            'monthly': 'price_1PuKQUBIjE5s9OuTVkUkTbZw',
            'yearly': None,
        },
        'Learned': {
            'monthly': 'price_1PuKQRBIjE5s9OuTsPuyJswr',
            'yearly': None,
        },
        'Lifetime': {
            'monthly': 'price_1PuKQQBIjE5s9OuTM6IzO22y',
            'yearly': 'price_1PuKQQBIjE5s9OuTM6IzO22y',
            'one_time': 'price_1PuKQQBIjE5s9OuTM6IzO22y',
        },
    }
    # STRIPE STUFF

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/steven/life-organizer-api/api/test.db'
    MONGODB_SETTINGS = {
        "db": "life-organizer-dev",
        "host": "mongodb://127.0.0.1:27019/life-organizer-dev"
    }

config = {
    'development': DevelopmentConfig,
    'docker-development': DockerDevelopmentConfig,
    'lan-docker-development': LANDockerDevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,
    # 'docker': DockerConfig,
    # 'unix': UnixConfig,

    'default': Config
}
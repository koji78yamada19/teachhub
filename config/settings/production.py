from .base import *
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1n%^5+e7@2@d74s0^j)$m*w)y%tcagh^+i&1*wn@m7(eqr0d=3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['deploy-test-yama.azurewebsites.net']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DB_ENGINE'),
#         'NAME': os.environ.get("DB_NAME"),
#         'USER': os.environ.get("DB_USER"),
#         'PASSWORD': os.environ.get("DB_PASSWORD"),
#         'HOST': os.environ.get("DB_HOST"),
#         'PORT': os.environ.get("DB_PORT"),
#         # 'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teachhub',
        'USER': 'sugiyama@teachhubsv',
        'PASSWORD': 'SJbGF9iAp6e2',
        'HOST': 'teachhubsv.postgres.database.azure.com',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


# 静的サーバーの設定（外部パッケージ利用する）
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = 'teachhubstr'
AZURE_ACCOUNT_KEY = '7SgcFtXHXjKvDJT/bLVqNzG/qePoW4SUtzsXlFqiW+KKmSp/lXYjVyj4rSaxLCOPmUqe1itw6mOMNw6fXrqb7Q=='
# AZURE_CUSTOM_DOMAIN = 'teachhubstr.blob.core.windows.net'
# AZURE_CONTAINER = 'app'
# STATIC_ROOT = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/static/'
# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/static/'
# MEDIA_ROOT = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/media/'
# MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/media/'

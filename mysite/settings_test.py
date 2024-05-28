from .settings import *  # Import the base settings

# Override the DATABASE setting to use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# Simplify password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Override the AWS storage to use local storage during tests
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# If there's no need to run email backend tests, use the LocMem email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Since static and media files handling is not typically tested in unit tests,
# you can comment out or adjust settings that won't affect your test outcomes
# STATICFILES_DIRS is overridden to an empty list to avoid issues during testing
STATICFILES_DIRS = []

# Disable Django-Heroku settings which might interfere with CI environment
# Comment out or remove the line that integrates Django-Heroku with settings
# django_heroku.settings(locals(), test_runner=False)

# Additionally, you may want to disable or modify other settings that are
# irrelevant or could interfere with testing in a CI environment.

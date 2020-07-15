import os

_translations_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "translations")

# Load Flask-User translations, if Flask-BabelEx has been installed
try:
    from flask_babelex import Domain

    # Retrieve Flask-User translations from the flask_user/translations directory
    domain_translations = Domain(_translations_dir, domain="wedding")
except ImportError:
    domain_translations = None


def gettext(string, **variables):
    return domain_translations.gettext(string, **variables) if domain_translations else string % variables


def lazy_gettext(string, **variables):
    return domain_translations.lazy_gettext(string, **variables) if domain_translations else string % variables

from flask import Blueprint

custom_jinja_blueprint: Blueprint = Blueprint("custom_jinja", __name__)

# # This is really annoying but we need to manually wire up the import chains to ensure that the
# # filters are correctly registered with the blueprint and to avoid circular imports
from .date import format_date

from datetime import date

from babel.dates import format_date as babel_format_date

from . import filters_blueprint


@filters_blueprint.app_template_filter()
def format_date(value: date, format: str = "long") -> str:
    return babel_format_date(value, format=format)

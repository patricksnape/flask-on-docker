from datetime import date, datetime
import calendar
from typing import List

from babel.dates import format_date as babel_format_date

from . import custom_jinja_blueprint


@custom_jinja_blueprint.app_template_filter()
def format_date(value: date, format: str = "long") -> str:
    return babel_format_date(value, format=format)


@custom_jinja_blueprint.app_template_global()
def calendar_matrix(value: date) -> List[List[int]]:
    return calendar.monthcalendar(value.year, value.month)


@custom_jinja_blueprint.app_template_global()
def now() -> datetime:
    return datetime.now()

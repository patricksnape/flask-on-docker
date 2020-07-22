from datetime import date

from babel.dates import format_date

from project import app


@app.template_filter()
def format_date(value: date, format: str = "long") -> str:
    return format_date(value, format)

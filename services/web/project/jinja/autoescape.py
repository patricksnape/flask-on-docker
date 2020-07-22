from typing import Optional


def select_jinja_autoescape(filename: Optional[str]) -> bool:
    """
    Returns `True` if autoescaping should be active for the given template name.

    Args:
        filename : Filename to validate

    Returns:
        Boolean indicating if file should be autoescaped
    """
    if filename is None:
        return False

    return filename.endswith(
        (
            ".html",
            ".htm",
            ".xml",
            ".xhtml",
            ".html.jinja",
            ".html.jinja2",
            ".xml.jinja",
            ".xml.jinja2",
            ".xhtml.jinja",
            ".xhtml.jinja2",
        )
    )

import secrets


def _invalid_token(token: str) -> bool:
    """
    A token is invalid if it contains a dash or an underscore.

    Args:
        token : Token to validate

    Returns:
        True if the token is invalid (e.g. it contains a '-' or '_')
    """
    return "-" in token or "_" in token


def get_token() -> str:
    """
    Generates a 6 character random string containing only upper case
    Alphanumeric characters.
    """
    token = secrets.token_urlsafe(4)
    while _invalid_token(token):
        token = secrets.token_urlsafe(4)

    assert len(token) == 6
    return token.upper()

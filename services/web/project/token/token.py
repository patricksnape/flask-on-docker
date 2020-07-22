import secrets


def get_token() -> str:
    """
    Generates a 6 character random string containing only upper case
    Alphanumeric characters.
    """
    token = secrets.token_urlsafe(4)
    while "-" in token:
        token = secrets.token_urlsafe(4)

    assert len(token) == 6
    return token.upper()

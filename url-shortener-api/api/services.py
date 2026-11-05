from config import settings


def extract_key(short_url: str) -> str:
    prefix = settings.ALIAS_BASE_URL.rstrip("/") + "/"

    if not short_url.startswith(prefix):
        raise ValueError("Invalid short URL")

    key = short_url[len(prefix) :]

    if not key:
        raise ValueError("Invalid short URL")

    return key

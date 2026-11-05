import pytest
from pytest_django import Settings

from api.services import extract_key


@pytest.fixture(autouse=True)
def alias_settings(settings: Settings) -> None:
    settings.ALIAS_BASE_URL = "http://localhost:8000/shrt/"


def test_key_extraction() -> None:
    assert extract_key("http://localhost:8000/shrt/qWeRtY12") == "qWeRtY12"


def test_key_extraction_invalid() -> None:
    with pytest.raises(ValueError):
        extract_key("http://someotherdomain.com/qWeRtY12")

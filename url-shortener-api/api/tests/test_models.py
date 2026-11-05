from unittest.mock import patch

import pytest

from api.models import URLAlias


@pytest.mark.django_db
def test_create_alias_with_unique_key() -> None:
    target_url = "http://example.com/very-very/long/url/even-longer"

    alias = URLAlias.objects.create_with_unique_key(target_url)

    assert alias.target_url == target_url
    assert len(alias.key) == URLAlias.KEY_LENGTH
    assert URLAlias.objects.filter(pk=alias.pk).exists()


@pytest.mark.django_db
def test_create_alias_retries_on_key_collision() -> None:

    URLAlias.objects.create(
        target_url="http://example.com/some/url",
        key="qwerty12",
    )

    with patch(
        "api.managers.get_random_string",
        side_effect=["qwerty12", "21ytrewq"],
    ) as mock_generate_key:
        alias = URLAlias.objects.create_with_unique_key(
            "http://example.com/very-very/long/url/even-longer"
        )

    assert alias.key == "21ytrewq"
    assert mock_generate_key.call_count == 2
    assert URLAlias.objects.count() == 2

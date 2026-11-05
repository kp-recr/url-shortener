import requests
from pytest_django.live_server_helper import LiveServer


def test_shorten_and_resolve_url(live_server: LiveServer) -> None:
    target_url = "http://example.com/very-very/long/url/even-longer"

    resource_url = f"{live_server.url}/api/short-urls"

    create_response = requests.post(
        f"{resource_url}/",
        json={"url": target_url},
        timeout=2,
    )

    assert create_response.status_code == 201

    created_alias = create_response.json()
    short_url = created_alias["short_url"]
    key = created_alias["key"]

    resolve_by_key_response = requests.get(
        f"{resource_url}/{key}/",
        timeout=2,
    )

    assert resolve_by_key_response.status_code == 200

    assert resolve_by_key_response.json()["target_url"] == target_url

    resolve_response = requests.get(
        f"{resource_url}/resolve/",
        params={"url": short_url},
        timeout=2,
    )

    assert resolve_response.status_code == 200

    assert resolve_response.json()["target_url"] == target_url

import requests
from pytest_django.live_server_helper import LiveServer


def test_shorten_and_resolve_url(live_server: LiveServer) -> None:
    target_url = "http://example.com/very-very/long/url/even-longer"

    resource_url = live_server.url + "/api/short-urls/"
    create_response = requests.post(
        resource_url,
        json={"url": target_url},
        timeout=2,
    )

    assert create_response.status_code == 201

    short_url = create_response.json()["short_url"]

    resolve_url = resource_url + "resolve"
    resolve_response = requests.get(
        resolve_url,
        params={"url": short_url},
        timeout=2,
    )

    assert resolve_response.status_code == 200

    assert resolve_response.json()["target_url"] == target_url

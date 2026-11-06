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


def test_validation_error_on_invalid_url(live_server: LiveServer) -> None:
    create_response = requests.post(
        f"{live_server.url}/api/short-urls/",
        json={"url": "invalid-url"},
        timeout=2,
    )

    assert create_response.status_code == 400


def test_required_field_error(live_server: LiveServer) -> None:
    create_response = requests.post(
        f"{live_server.url}/api/short-urls/",
        json={"something": "elseurl"},
        timeout=2,
    )

    assert create_response.status_code == 400
    assert "url" in create_response.json()


def test_unexisting_alias_by_key(live_server: LiveServer) -> None:
    response = requests.get(
        f"{live_server.url}/api/short-urls/unexisting-key/",
        timeout=2,
    )

    assert response.status_code == 404


def test_unexisting_alias_by_url(live_server: LiveServer) -> None:
    resolve_response = requests.get(
        f"{live_server.url}/api/short-urls/resolve/",
        params={"url": "http://someotherdomain.com/asecefewrf"},
        timeout=2,
    )

    assert resolve_response.status_code == 400
    assert "url" in resolve_response.json()

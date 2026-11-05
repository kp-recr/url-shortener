### URL Shortener API

A basic URL shortening API, written with Django Rest Framework.

#### Start application (Docker)

To start the application in a development environment:

```bash
cp url-shortener-api/.env-example url-shortener-api/.env
```

```bash
make up
```

The short URL base can be configured using the ALIAS_BASE_URL environment variable.

---

### Initial setup

After starting the application, run migrations:

```bash
make docker-migrate
```

---

#### API

Base URL: `http://localhost:8000`

To shorten a URL:

POST `/api/short-urls/`

```json
{
  "url": "http://example.com/some/too/long/url"
}
```

Output:

```json
{
  "short_url": "http://localhost:8000/shrt/Nw36LwrM",
  "key": "Nw36LwrM"
}
```

To get it back, either use the `key`

GET /api/short-urls/Nw36LwrM/

or resolve it by short URL:

GET /api/short-urls/resolve/

with query parameter:

```
url = http://localhost:8000/shrt/Nw36LwrM
```

Output for both:

```json
{
  "target_url": "http://example.com/some/too/long/url"
}
```

---

#### Tests

```bash
make docker-test
```

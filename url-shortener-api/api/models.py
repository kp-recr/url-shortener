from django.db import models

from api.managers import URLAliasManager


class URLAlias(models.Model):
    "Stores unique and short alias (key) for a given URL"

    KEY_LENGTH = 8

    key = models.CharField(max_length=KEY_LENGTH, unique=True)
    target_url = models.URLField(unique=True)

    objects = URLAliasManager()

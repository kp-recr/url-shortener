from typing import TYPE_CHECKING

from django.db import IntegrityError, models, transaction
from django.utils.crypto import get_random_string

if TYPE_CHECKING:
    from api.models import URLAlias


class URLAliasManager(models.Manager):

    RETRY_COUNT = 5

    def create_with_unique_key(self, target_url: str) -> URLAlias:
        for _ in range(self.RETRY_COUNT):
            key = get_random_string(length=self.model.KEY_LENGTH)

            try:
                with transaction.atomic():
                    return self.create(
                        target_url=target_url,
                        key=key,
                    )
            except IntegrityError:
                if self.filter(key=key).exists():
                    # The error was due to key collision, generate again
                    continue
                raise

        raise RuntimeError("Couldn't generate unique key")

from typing import Any

from rest_framework import serializers

from api.models import URLAlias
from config import settings


class ShortURLCreateSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source="target_url", write_only=True)
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = URLAlias
        fields = ["url", "short_url"]

    def get_short_url(self, url_alias: URLAlias) -> str:
        base_url = settings.ALIAS_BASE_URL.rstrip("/")
        return f"{base_url}/{url_alias.key}"

    def create(self, validated_data: dict[str, Any]) -> URLAlias:
        return URLAlias.objects.create_with_unique_key(**validated_data)


class ShortURLResolveSerializer(serializers.Serializer):
    url = serializers.URLField()

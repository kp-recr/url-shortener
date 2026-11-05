from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import URLAlias
from api.serializers import (
    ShortURLCreateSerializer,
    ShortURLResolveSerializer,
)
from api.services import extract_key


@api_view(["POST"])
def create_short_url(request: Request) -> Response:
    serializer = ShortURLCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    target_url = serializer.validated_data["target_url"]

    existing_alias = URLAlias.objects.filter(target_url=target_url).first()

    if existing_alias is not None:
        return Response(ShortURLCreateSerializer(existing_alias).data)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def resolve_short_url(request: Request) -> Response:
    serializer = ShortURLResolveSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    url = serializer.validated_data["url"]
    try:
        key = extract_key(url)
    except ValueError as value_error:
        raise serializers.ValidationError({"url": str(value_error)}) from value_error

    url_alias = get_object_or_404(URLAlias, key=key)

    return Response({"target_url": url_alias.target_url})


@api_view(["GET"])
def resolve_short_url_by_key(request: Request, key: str) -> Response:
    url_alias = get_object_or_404(URLAlias, key=key)

    return Response({"target_url": url_alias.target_url})

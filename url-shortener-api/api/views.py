from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import URLAlias
from api.serializers import ShortURLCreateSerializer


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

from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.views import Response
from rest_framework.viewsets import ViewSet
from rockapi.models import Rock


class RockView(ViewSet):
    """Rock view set"""

    def create(self, request):
        return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        try:
            rocks = Rock.objects.all()
            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rock
        fields = (
            "id",
            "name",
            "weight",
        )

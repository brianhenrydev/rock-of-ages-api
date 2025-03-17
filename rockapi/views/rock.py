from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.views import Response
from rest_framework.viewsets import ViewSet
from rockapi.models import Rock
from rockapi.models import Type


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


class RockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("label",)


class RockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class RockSerializer(serializers.ModelSerializer):
    type = RockTypeSerializer(many=False)

    user = RockUserSerializer(many=False)

    class Meta:
        model = Rock
        fields = (
            "id",
            "name",
            "weight",
            "user",
            "type",
        )

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
        chosen_type = Type.objects.get(pk=request.data["typeId"])
        rock = Rock()
        rock.user = request.auth.user
        rock.weight = request.data["weight"]
        rock.name = request.data["name"]
        rock.type = chosen_type
        rock.save()
        serialized = RockSerializer(rock, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        owner_only = self.request.query_params.get("owner", None)
        weight = self.request.query_params.get("weight", None)
        rock_type = self.request.query_params.get("type", None)

        try:
            rocks = Rock.objects.all()

            if owner_only is not None and owner_only == "current":
                rocks = rocks.filter(user=request.auth.user)

            if weight is not None and weight == "light":
                rocks = rocks.filter(weight__lte=3)

            elif weight is not None and weight == "mid":
                rocks = rocks.filter(weight__gt=3, weight__lte=9)

            elif weight is not None and weight == "heavy":
                rocks = rocks.filter(weight__gt=9)

            if rock_type is not None:
                rocks = rocks.filter(type=rock_type)

            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        try:
            rock = Rock.objects.get(pk=pk)
            serializer = RockSerializer(rock, many=False)
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"Rock not found": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rock = Rock.objects.get(pk=pk)
            if rock.user.id == request.auth.user.id:
                rock.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message": "You do not own that rock"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except rock.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("label",)


class RockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


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

from rest_framework.generics import CreateAPIView

from computer.api.serializers import ComputerSerializer


# Create your views here.
class ComputerAPIView(CreateAPIView):
    serializer_class = ComputerSerializer


# TODO: create update and delete APIview

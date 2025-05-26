from rest_framework.generics import CreateAPIView

from .serializers import ComputerSerializer


# Create your views here.
class ComputerAPIView(CreateAPIView):
    serializer_class = ComputerSerializer

# TODO: create update and delete view

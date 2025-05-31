from rest_framework import serializers

from chat.models import Computer


class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ("name", "nickname", "password")

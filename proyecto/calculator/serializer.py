from rest_framework import serializers


class newSerializer(serializers.Serializer):
   id = serializers.CharField()
   name = serializers.CharField()

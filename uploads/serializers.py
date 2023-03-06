from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    directory = serializers.CharField(required=True, min_length=4)
    file = serializers.FileField()
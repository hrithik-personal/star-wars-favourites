from rest_framework import serializers


class PlanetSerializer(serializers.Serializer):
    name = serializers.CharField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    url = serializers.URLField()
    is_favourite = serializers.BooleanField()
    
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data

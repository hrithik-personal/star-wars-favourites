from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField()
    release_date = serializers.DateField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    url = serializers.URLField()
    is_favourite = serializers.BooleanField()
    
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data

from rest_framework import serializers

from .models import Movie

class MovieIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'poster'
        )
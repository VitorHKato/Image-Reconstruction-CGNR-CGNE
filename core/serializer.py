from rest_framework import serializers

from .models import Request

class RequestSerializer(serializers.Serializer):
    class Meta:
        model = Request
        fields = (
            'image',
            'user_id',
            'user_name',
            'image_pixel_size',
            'algorithm_name',
            'iterations'
        )

    def create(self, validated_data):
        return Request.objects.create(**self.initial_data)


class RequestSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'image',
            'user_id',
            'user_name',
            'image_pixel_size',
            'algorithm_name',
            'iterations'
        )


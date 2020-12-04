
from rest_framework import serializers
from home.models import result


class ZillowSerializer(serializers.ModelSerializer):
    class Meta:
        model = result
        fields = '__all__'
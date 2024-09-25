from rest_framework import serializers
from .models import SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'timestamp', 'temperature', 'humidity']
        # You can use extra_kwargs to make fields required if necessary
        extra_kwargs = {
            'temperature': {'required': True},
            'humidity': {'required': True}
        }

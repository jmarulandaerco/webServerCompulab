from rest_framework import serializers
from energyAPP.models import WeatherStationData

class WeatherStationSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeatherStationData model.

    This serializer automatically includes all fields from the WeatherStationData model,
    allowing for easy conversion between model instances and JSON representations,
    as well as input validation for API requests.

    Meta:
        model: The WeatherStationData model to serialize.
        fields: Includes all fields from the model.
    """
    class Meta:
        model = WeatherStationData
        fields = '__all__'  # Esto incluye todos los campos del modelo

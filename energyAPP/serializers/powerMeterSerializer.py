from rest_framework import serializers
from energyAPP.models import WeatherStationData
from energyAPP.models.powerMeterModel import PowerMeterData

class PowerMeterSerializer(serializers.ModelSerializer):
    """
    Serializer for the PowerMeterSerializer model.

    This serializer automatically includes all fields from the PowerMeterSerializer model,
    allowing for easy conversion between model instances and JSON representations,
    as well as input validation for API requests.

    Meta:
        model: The PowerMeterSerializer model to serialize.
        fields: Includes all fields from the model.
    """
    class Meta:
        model = PowerMeterData
        fields = '__all__'  # Esto incluye todos los campos del modelo

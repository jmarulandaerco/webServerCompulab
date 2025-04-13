from rest_framework import serializers
from energyAPP.models import InverterData

class InverterDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the InverterData model.

    This serializer automatically includes all fields from the InverterData model,
    allowing for easy conversion between model instances and JSON representations,
    as well as input validation for API requests.

    Meta:
        model: The InverterData model to serialize.
        fields: Includes all fields from the model.
    """
    class Meta:
        model = InverterData
        fields = '__all__'  # Esto incluye todos los campos del modelo

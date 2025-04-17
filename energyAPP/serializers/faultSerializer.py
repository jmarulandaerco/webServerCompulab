from rest_framework import serializers
from energyAPP.models import InverterData
from energyAPP.models.faultModel import FaultData

class FaultDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the FaultData model.

    This serializer automatically includes all fields from the FaultData model,
    allowing for easy conversion between model instances and JSON representations,
    as well as input validation for API requests.

    Meta:
        model: The FaultData model to serialize.
        fields: Includes all fields from the model.
    """
    class Meta:
        model = FaultData
        fields = '__all__'  # Esto incluye todos los campos del modelo

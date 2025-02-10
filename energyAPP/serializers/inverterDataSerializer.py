from rest_framework import serializers
from energyAPP.models import InverterData

class InverterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InverterData
        fields = '__all__'  # Esto incluye todos los campos del modelo

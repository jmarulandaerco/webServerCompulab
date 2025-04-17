from djongo import models

class InverterData(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Único campo autogenerado
    send_server = models.BooleanField(default=True)
    DATE = models.DateTimeField()
    TP_I = models.IntegerField()
    OPERATION_STATE = models.IntegerField()
    GENERATION = models.FloatField()
    POWER_FACTOR = models.FloatField()
    REACTIVE_POWER = models.FloatField()
    POWER_SNAPSHOT = models.FloatField()
    VOLTAGE_1_DC = models.FloatField()
    VOLTAGE_2_DC = models.FloatField()
    VOLTAGE_3_DC = models.FloatField()
    VOLTAGE_4_DC = models.FloatField()
    CURRENT_1_DC = models.FloatField()
    CURRENT_2_DC = models.FloatField()
    CURRENT_3_DC = models.FloatField()
    CURRENT_4_DC = models.FloatField()
    VOLTAGE_1_AC = models.FloatField()
    VOLTAGE_2_AC = models.FloatField()
    VOLTAGE_3_AC = models.FloatField()
    CURRENT_1_AC = models.FloatField()
    CURRENT_2_AC = models.FloatField()
    CURRENT_3_AC = models.FloatField()
    TEMPERATURE_INVERTER = models.FloatField()
    GRID_FREQUENCY = models.FloatField()
    id_slave = models.IntegerField()
    device_type = models.CharField(max_length=255)
    sent = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "inverters"

    def __str__(self):
        return f"Inverter Data {self._id}"

from djongo import models

class PowerMeterData(models.Model):
    """
    Model representing data collected from a power meter device.

    Fields:
        _id (ObjectIdField): Automatically generated unique identifier for the document.
        send_server (BooleanField): Indicates whether the data should be sent to the server.
        DATE (DateTimeField): The date and time the data was recorded.
        TP_I (FloatField): TP_I value, possibly current or a derived metric.
        APPARENT_POWER (FloatField): Apparent power in volt-amperes (VA).
        POWER_SNAPSHOT (FloatField): Real power snapshot in watts (W).
        REACTIVE_POWER (FloatField): Reactive power in vars (VAr).
        POWER_FACTOR (FloatField): Power factor (ratio).
        id_slave (IntegerField): Identifier of the slave device that reported the data.
        id_inserted (ObjectIdField): Reference to the ID of the document or entity that inserted the data.
        device_type (CharField): Type of device (e.g., 'power_meter').
        sent (BooleanField): Indicates whether the data has been successfully sent.

    Meta:
        db_table (str): Specifies the MongoDB collection name ('power_meters').

    Methods:
        __str__(): Returns a human-readable representation of the model instance.
    """
    _id = models.ObjectIdField(primary_key=True)
    send_server = models.BooleanField(default=True)
    DATE = models.DateTimeField()
    TP_I = models.FloatField()
    APPARENT_POWER = models.FloatField()
    POWER_SNAPSHOT = models.FloatField()
    REACTIVE_POWER = models.FloatField()
    POWER_FACTOR = models.FloatField()
    id_slave = models.IntegerField()
    device_type = models.CharField(max_length=255)
    sent = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "power_meters"

    def __str__(self):
        return f"Power Meter Data {self._id}"

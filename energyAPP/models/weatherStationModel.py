from djongo import models

class WeatherStationData(models.Model):
    """
    Model representing data collected from a weather station device.

    Fields:
        _id (ObjectIdField): Automatically generated unique identifier for the document.
        send_server (BooleanField): Indicates whether the data should be sent to the server.
        DATE (DateTimeField): The date and time the data was recorded.
        IRRADIANCE (FloatField): Solar irradiance in W/m².
        TEMPERATURE_ENVIRONMENT (FloatField): Ambient temperature in degrees Celsius.
        TEMPERATURE_PANEL (FloatField): Temperature of the solar panel in degrees Celsius.
        id_slave (IntegerField): Identifier of the slave device that reported the data.
        id_inserted (ObjectIdField): Reference to the ID of the document or entity that inserted the data.
        device_type (CharField): Type of device (e.g., 'weather_station').
        sent (BooleanField): Indicates whether the data has been successfully sent.

    Meta:
        db_table (str): Specifies the MongoDB collection name ('weather_stations').

    Methods:
        __str__(): Returns a human-readable representation of the model instance.
    """
    _id = models.ObjectIdField(primary_key=True)  # Campo autogenerado
    send_server = models.BooleanField(default=True)
    DATE = models.DateTimeField()
    IRRADIANCE = models.FloatField()
    TEMPERATURE_ENVIRONMENT = models.FloatField()
    TEMPERATURE_PANEL = models.FloatField()
    id_slave = models.IntegerField()
    device_type = models.CharField(max_length=255)
    sent = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "weather_stations"

    def __str__(self):
        return f"Weather Station Data {self._id}"

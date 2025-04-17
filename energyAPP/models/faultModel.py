from djongo import models

class FaultData(models.Model):
    """
    Model representing fault data reported by a device.

    Fields:
        _id (ObjectIdField): Automatically generated unique identifier for the document.
        id_inserted (ObjectIdField): Reference to the entity that inserted the data.
        device_id (ObjectIdField): Identifier of the device that reported the fault.
        device_type (CharField): Type of device, expected to be 'fault'.
        DATE (DateTimeField): The timestamp when the fault was reported.
        F1 (FloatField): Fault indicator 1 (can be null).
        F2 (FloatField): Fault indicator 2 (can be null).
        F3 (FloatField): Fault indicator 3 (can be null).
        sent (BooleanField): Whether the fault data has been sent to the server.

    Meta:
        db_table (str): Specifies the MongoDB collection name ('fault_data').

    Methods:
        __str__(): Returns a human-readable representation of the model instance.
    """
    _id = models.ObjectIdField(primary_key=True)
    device_type = models.CharField(max_length=100)
    DATE = models.DateTimeField()
    F1 = models.FloatField(null=True, blank=True)
    F2 = models.FloatField(null=True, blank=True)
    F3 = models.FloatField(null=True, blank=True)
    sent = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "fault_data"

    def __str__(self):
        return f"Fault Report {self._id}"

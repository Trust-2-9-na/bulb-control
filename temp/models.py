from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField(default=0.0)  # Ensure this field is present and has a default value

    def __str__(self):
        return f"SensorData at {self.timestamp} - Temp: {self.temperature}°C, Humidity: {self.humidity}%"

from django.db import models

class BulbControl(models.Model):
    STATUS_CHOICES = [
        ('ON', 'On'),
        ('OFF', 'Off'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='OFF')

    def __str__(self):
        return f"Bulb {self.get_status_display()} at {self.timestamp.isoformat()}"


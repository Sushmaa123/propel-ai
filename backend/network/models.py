from django.db import models


class Feeder(models.Model):
    feeder_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DistributionTransformer(models.Model):
    transformer_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    feeder = models.ForeignKey(
        Feeder,
        on_delete=models.CASCADE,
        related_name="transformers"
    )

    def __str__(self):
        return self.name


class Pole(models.Model):
    pole_id = models.CharField(max_length=50, unique=True)
    sequence_number = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    transformer = models.ForeignKey(
        DistributionTransformer,
        on_delete=models.CASCADE,
        related_name="poles"
    )

    def __str__(self):
        return self.pole_id


class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)

    pole = models.OneToOneField(
        Pole,
        on_delete=models.CASCADE,
        related_name="device"
    )

    def __str__(self):
        return self.device_id
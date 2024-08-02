from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    have_projector = models.BooleanField()


class Booking(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = (('room_id', 'date'),)

from django.db import models
from UserProfile.models import UserProfile
from Contract.models import Contract


class Event(models.Model):
    """Database Event model"""
    ee_contact = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    contract = models.OneToOneField(Contract, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.IntegerField(max_length=10)
    notes = models.TextField(max_length=2000)

    def __str__(self) -> str:
        """returns event info"""
        return f"event: {self.name}, date_start: {self.date_start}, attendees: {self.attendees}"

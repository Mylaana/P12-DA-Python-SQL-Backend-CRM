from django.db import models
from UserProfile.models import UserProfile
from Client.models import Client



class Contract(models.Model):
    """Database contract model"""
    ee_contact = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    information = models.CharField(max_length=100, unique=True)
    value_total_price = models.FloatField(max_length=12)
    value_rest_to_pay = models.FloatField(max_length=12)
    date_creation = models.DateTimeField(auto_now_add=True)
    status_is_active = models.BooleanField(default=True)


    def __str__(self) -> str:
        """returns contact info"""
        return (
            f"client name: {self.client.name}, information: {self.information} active: {self.status_is_active}"
        )

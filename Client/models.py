from django.db import models
from UserProfile.models import UserProfile


class Client(models.Model):
    """Database client model"""
    ee_contact = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, unique=True)
    siren = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    client_contact_name = models.CharField(max_length=100)
    information = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        """returns Client info"""
        return (
            f"username: {self.name}, email: {self.email},"
            f" phone: {self.phone}, client contact name: {self.client_contact_name}"
        )

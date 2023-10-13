from django.db import models
from UserProfile.models import UserProfile



class Client(models.Model):
    """Database user model"""
<<<<<<< HEAD
    ee_contact = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
=======
    ee_contact = models.ForeignKey(Userprofile, null=True, on_delete=models.SET_NULL)
>>>>>>> clients_model
    name = models.CharField(max_length=100, unique=True)
    siren = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    client_contact_name = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        """returns Client contact info"""
        return (
            f"username: {self.name}, email: {self.email},"
            f" phone: {self.phone}, client contact name: {self.client_contact_name}"
        )

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserProfileManager(BaseUserManager):
    """Database User Manager model"""

    def create_user(self, username, email, first_name, last_name, phone, password=None):
        """Create user in database"""

        if not email:
            raise ValueError("User must have an email adress")

        if not first_name:
            raise ValueError("please provide user's first name")

        if not last_name:
            raise ValueError("please provide user's last name")

        if not phone:
            raise ValueError("please provide user's phone number")

        email = self.normalize_email(email)

        user = self.model(username=username,
                          email=email,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password):
        """Create superuser in database"""

        user = self.create_user(username=username, email=email, first_name=first_name,
                                last_name=last_name, phone=phone, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database user model"""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    #add Foreign key to team

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # The CRM is expecting only staff users but can be set to false
    is_staff = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

    def __str__(self) -> str:
        """returns user contact info"""
        return f"username: {self.username}, email: {self.email}, phone: {self.phone}"

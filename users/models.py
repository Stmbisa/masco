"""
Database models
"""

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone



class UserManager(BaseUserManager):
    """ minimum fields for all users"""
    def create_user(
            self,
            email,
            telephone,
            username,
            first_name,
            last_name,
            password=None,
            **extra_fields):
        if not email:
            raise ValueError('You need to provide an email address')

        if not telephone:
            raise ValueError('You need to provide a telephone')

        if not username:
            raise ValueError('You need to set a username')

        """ calling the model this manager is responsible for with self.model."""
        user = self.model(
            email= self.normalize_email(email),
            telephone =telephone,
            username = username,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            username,
            first_name,
            last_name,
            password,
            telephone,
            **extra_fields):
        """ calling the create_user method """
        user =self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            telephone=telephone,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system. """
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    families = models.ManyToManyField('self')
    """ required fields """
    date_joined = models.DateTimeField(auto_now= True)
    last_login = models.DateTimeField(auto_now= True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    id_telephone_verified = models.IntegerField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'telephone']

    def is_membership_active(self):
        """Check if user's membership is currently active."""
        today = timezone.now().date()
        return self.membership_start_date <= today <= self.membership_end_date

    def send_membership_expiry_email(self):
        """Send an email to the user if their membership is about to expire."""
        days_until_expiry = (self.booking_set.filter(membership__membership_end_date__gte=timezone.now().date())
                            .earliest('membership__membership_end_date')
                            .membership_end_date - timezone.now().date()).days
        if days_until_expiry == 2:
            subject = "Your gym membership is about to expire"
            message = render_to_string('membership_expiry_email.html', {'user': self})
            send_mail(subject, message, 'gym@example.com', [self.email])

    def __str__(self):
        return self.first_name + " " + self.last_name


class Trainer(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name=models.CharField(max_length=55)
    gender=models.CharField(max_length=25)
    phone=models.CharField(max_length=25)
    salary=models.IntegerField()
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.first_name + " " + self.last_name

    






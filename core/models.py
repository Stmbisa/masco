from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

class BMI(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_bmi(self):
        return self.weight / ((self.height / 100) ** 2)
    

class Subscription(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey('Membership', on_delete=models.CASCADE)
    session_date = models.DateField()
    session_type = models.CharField(max_length=50) # type of session (e.g. private training session, class session, etc.)

    def __str__(self):
        return f"{self.user.first_name} booked a {self.session_type} session on {self.session_date}"

    def is_sunday_booking(self):
        # check if session_date is a Sunday
        if self.session_date.weekday() == 6:
            return True
        else:
            return False
        

class Membership(models.Model):
    MEMBERSHIP_TYPES = (
        ('private', 'Private'),
        ('monthly', 'Monthly'),
    )

    type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='private')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField(default=30, editable=False)




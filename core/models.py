from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, time, timedelta
from django.utils import timezone



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
    
class Membership(models.Model):
    MEMBERSHIP_TYPES = (
        ('private', 'Private'),
        ('monthly', 'Monthly'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='private')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField(default=30,)
    has_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def is_membership_active(self):
        """Check if the membership is active since the day they signed up for it."""
        if self.is_active:
            today = timezone.now().date()
            days_since_signup = (today - self.created_date).days
            if days_since_signup <= self.duration:
                return True
            else:
                return False
        else:
            return False

    def is_membership_paid(self):
        """Check if the membership is paid for."""
        return self.has_paid

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    session_date = models.DateField()
    session_start_time = models.TimeField(default=timezone.now)
    session_end_time = models.TimeField(default=timezone.now)
    SSESSION_TYPES = (
        ('private', 'Private'),
        ('gym', 'gym'),
    )
    session_type = models.CharField(max_length=10, choices=SSESSION_TYPES, default='gym') # type of session (e.g. private training session, class session, etc.)

    def __str__(self):
        return f"{self.user.first_name} booked a {self.session_type} session on {self.session_date}"

    def is_sunday_booking(self):
        # check if session_date is a Sunday
        if self.session_date.weekday() == 6:
            return True
        else:
            return False
        
    def get_booked_hours(self):
        # get all bookings for the same session date and session type
        bookings = Booking.objects.filter(session_date=self.session_date, session_type=self.session_type)

        # create a set to store booked hours
        booked_hours = set()

        # iterate through each booking and add the booked hours to the set
        for booking in bookings:
            start_time = booking.session_start_time
            end_time = booking.session_end_time
            hours_range = range(start_time.hour, end_time.hour + 1)
            booked_hours.update(hours_range)

        # return the set of booked hours
        return booked_hours
        
    def is_available(self):
        """Check if session time is available and the day is not sold out."""
        start_time = datetime.combine(self.session_date, self.session_start_time)
        end_time = datetime.combine(self.session_date, self.session_end_time)
        bookings_on_day = Booking.objects.filter(session_date=self.session_date, session_type=self.session_type)
        
        # Check if day is sold out
        if bookings_on_day.count() >= 6:
            return False
        
        # Check for overlapping bookings
        for booking in bookings_on_day:
            booking_start_time = datetime.combine(booking.session_date, booking.session_start_time)
            booking_end_time = datetime.combine(booking.session_date, booking.session_end_time)
            if (start_time < booking_end_time) and (end_time > booking_start_time):
                return False
        
        return True

        



class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s testimonial"
    

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    
class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField(blank=False, null=False)
    phonenumber=models.CharField(max_length=12, blank=False, null=False)
    subject=models.TextField(max_length=100, blank=True)
    message=models.TextField()

    def __str__(self):
        return self.email
    
from django.db import models
from django.contrib.auth import get_user_model
import django



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
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
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
        
    def is_available(self):
        """Check if session time is available and the day is not sold out."""
        session_time = self.session_date.time()
        bookings_on_day = Booking.objects.filter(session_date=self.session_date, session_type=self.session_type)
        if bookings_on_day.count() >= 6:
            return False  # Day is sold out
        if bookings_on_day.filter(session_date__time=session_time).exists():
            return False  # Session time is booked
        return True
        



class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    


    
    




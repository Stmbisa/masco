from django.db import models

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


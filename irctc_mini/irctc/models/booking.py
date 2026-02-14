from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .auth import User
from .train import Train

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='bookings')
    passenger_name = models.CharField(max_length=255)
    passenger_email = models.EmailField()
    passenger_phone = models.CharField(max_length=15)
    seats_booked = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = 'bookings'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['train']),
            models.Index(fields=['booking_date']),
        ]
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.email} - {self.train.train_number}"
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Train(models.Model):
    train_number = models.CharField(max_length=20, unique=True)
    train_name = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    fare = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trains'
        ordering = ['departure_time']
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['train_number']),
            models.Index(fields=['active']),
        ]
    
    def __str__(self):
        return f"{self.train_number} - {self.train_name}"
    
    def save(self, *args, **kwargs):
        # Ensure available_seats never exceeds total_seats
        if self.available_seats > self.total_seats:
            self.available_seats = self.total_seats
        
        # Ensure available_seats is never negative
        if self.available_seats < 0:
            self.available_seats = 0
        
        super().save(*args, **kwargs)
    
    def has_available_seats(self, seats_requested):
        """
        Check if train has enough available seats
        """
        return self.available_seats >= seats_requested and self.active
    
    def book_seats(self, seats_count):
        """
        Deduct seats from available seats
        """
        if self.has_available_seats(seats_count):
            self.available_seats -= seats_count
            self.save()
            return True
        return False
    
    def cancel_seats(self, seats_count):
        """
        Add seats back to available seats (on cancellation)
        """
        self.available_seats = min(self.available_seats + seats_count, self.total_seats)
        self.save()
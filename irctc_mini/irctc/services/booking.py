from ..models.booking import Booking
from ..models.train import Train
from django.db import transaction
from django.utils import timezone

class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(user, train_id, passenger_name, passenger_email, 
                      passenger_phone, seats_booked):
        """
        Create a new booking with seat validation
        """
        try:
            train = Train.objects.select_for_update().get(id=train_id)
        except Train.DoesNotExist:
            return None
        
        # Check if train has enough seats
        if not train.has_available_seats(seats_booked):
            return None
        
        # Calculate total amount
        total_amount = train.fare * seats_booked
        
        # Create booking
        booking = Booking.objects.create(
            user=user,
            train=train,
            passenger_name=passenger_name,
            passenger_email=passenger_email,
            passenger_phone=passenger_phone,
            seats_booked=seats_booked,
            total_amount=total_amount
        )
        
        # Deduct seats from train
        train.book_seats(seats_booked)
        
        return booking
    
    @staticmethod
    @transaction.atomic
    def cancel_booking(booking_id):
        """
        Cancel a booking and return seats to train
        """
        try:
            booking = Booking.objects.select_for_update().get(id=booking_id)
        except Booking.DoesNotExist:
            return None
        
        if booking.status == 'cancelled':
            return booking
        
        # Add seats back to train
        train = booking.train
        train.cancel_seats(booking.seats_booked)
        
        # Update booking status
        booking.status = 'cancelled'
        booking.save()
        
        return booking
    
    @staticmethod
    def get_user_bookings(user):
        """
        Get all bookings for a user
        """
        return Booking.objects.filter(user=user).order_by('-booking_date')
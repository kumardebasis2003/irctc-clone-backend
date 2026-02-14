from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from irctc.services import booking as booking_services
from irctc.services import auth as auth_services
from irctc.serializers import booking as booking_serializers
from irctc.models import booking as booking_models

class BookingCreateView(APIView):
    """
    Create a new booking (No MongoDB logging)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Validate request data
        serializer = booking_serializers.BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create booking using service
        booking = booking_services.BookingService.create_booking(
            user=request.user,
            train_id=serializer.validated_data['train_id'],
            passenger_name=serializer.validated_data['passenger_name'],
            passenger_email=serializer.validated_data['passenger_email'],
            passenger_phone=serializer.validated_data['passenger_phone'],
            seats_booked=serializer.validated_data['seats_booked']
        )
        
        if not booking:
            return Response(
                {'error': 'Failed to create booking. Check seat availability'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            booking_serializers.BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )

class UserBookingsView(ListAPIView):
    """
    Get all bookings for the logged-in user
    """
    serializer_class = booking_serializers.BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return booking_services.BookingService.get_user_bookings(self.request.user)

class BookingDetailView(APIView):
    """
    Get detailed information about a specific booking
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, booking_id):
        booking = booking_services.BookingService.get_booking_by_id(booking_id)
        
        if not booking:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user owns this booking
        if booking.user != request.user and not auth_services.UserService.is_admin(request.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
            booking_serializers.BookingSerializer(booking).data,
            status=status.HTTP_200_OK
        )

class BookingCancelView(APIView):
    """
    Cancel a booking (No MongoDB logging)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, booking_id):
        # Get booking by ID
        booking = booking_services.BookingService.get_booking_by_id(booking_id)
        
        if not booking:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user owns this booking
        if booking.user != request.user and not auth_services.UserService.is_admin(request.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cancel booking using service
        cancelled_booking = booking_services.BookingService.cancel_booking(booking_id)
        
        if not cancelled_booking:
            return Response(
                {'error': 'Failed to cancel booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            booking_serializers.BookingSerializer(cancelled_booking).data,
            status=status.HTTP_200_OK
        )

class AllBookingsView(ListAPIView):
    """
    Get all bookings (Admin only)
    """
    serializer_class = booking_serializers.BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only admin can view all bookings
        if not auth_services.UserService.is_admin(self.request.user):
            return booking_models.Booking.objects.none()
        
        return booking_services.BookingService.get_active_bookings()
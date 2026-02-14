from rest_framework import serializers
from irctc.models import train as train_models
from irctc.models import booking as booking_models

class BookingSerializer(serializers.ModelSerializer):
    train = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = booking_models.Booking
        fields = [
            'id', 'user', 'train', 'passenger_name', 'passenger_email', 
            'passenger_phone', 'seats_booked', 'booking_date', 'status', 'total_amount'
        ]
        read_only_fields = ['id', 'booking_date']
    
    def get_train(self, obj):
        train = obj.train
        return {
            'id': train.id,
            'train_number': train.train_number,
            'train_name': train.train_name,
            'source': train.source,
            'destination': train.destination,
            'departure_time': train.departure_time,
            'arrival_time': train.arrival_time,
            'available_seats': train.available_seats,
            'fare': train.fare
        }
    
    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    
    def validate_seats_booked(self, value):
        # This will be validated in the service layer
        return value

class BookingCreateSerializer(serializers.Serializer):
    train_id = serializers.IntegerField()
    passenger_name = serializers.CharField(max_length=255)
    passenger_email = serializers.EmailField()
    passenger_phone = serializers.CharField(max_length=15)
    seats_booked = serializers.IntegerField(min_value=1)
    
    def validate(self, data):
        try:
            train = train_models.Train.objects.get(id=data['train_id'])
        except train_models.Train.DoesNotExist:
            raise serializers.ValidationError("Train not found")
        
        if not train.has_available_seats(data['seats_booked']):
            raise serializers.ValidationError("Not enough seats available")
        
        return data

class BookingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user bookings (lightweight)
    """
    train_number = serializers.CharField(source='train.train_number', read_only=True)
    train_name = serializers.CharField(source='train.train_name', read_only=True)
    source = serializers.CharField(source='train.source', read_only=True)
    destination = serializers.CharField(source='train.destination', read_only=True)
    
    class Meta:
        model = booking_models.Booking
        fields = [
            "id",
            "train_number",
            "train_name",
            "source",
            "destination",
            "passenger_name",
            "seats_booked",
            "booking_date",
            "status",
            "total_amount",
        ]
        read_only_fields = ["id"]

class BookingCancelSerializer(serializers.Serializer):
    """
    Serializer for cancelling a booking
    """
    booking_id = serializers.IntegerField(
        help_text="ID of the booking to cancel"
    )
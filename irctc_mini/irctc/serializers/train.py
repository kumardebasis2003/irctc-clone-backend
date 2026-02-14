from rest_framework import serializers
from irctc.models import train as train_models

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = train_models.Train
        fields = [
            'id', 'train_number', 'train_name', 'source', 'destination',
            'departure_time', 'arrival_time', 'total_seats',
            'available_seats', 'fare', 'active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Ensure departure time is before arrival time
        if 'departure_time' in data and 'arrival_time' in data:
            if data['departure_time'] >= data['arrival_time']:
                raise serializers.ValidationError(
                    "Departure time must be before arrival time"
                )
        
        # Ensure available seats doesn't exceed total seats
        if 'total_seats' in data and 'available_seats' in data:
            if data['available_seats'] > data['total_seats']:
                raise serializers.ValidationError(
                    "Available seats cannot exceed total seats"
                )
        
        return data

class TrainSearchSerializer(serializers.Serializer):
    source = serializers.CharField(required=True, max_length=100)
    destination = serializers.CharField(required=True, max_length=100)
    date = serializers.DateField(required=False)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=100)
    offset = serializers.IntegerField(required=False, default=0, min_value=0)
    
class TrainListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing trains (lightweight)
    """
    class Meta:
        model = train_models.Train
        fields = [
            "id",
            "train_number",
            "train_name",
            "source",
            "destination",
            "departure_time",
            "arrival_time",
            "available_seats",
            "fare",
            "active",
        ]
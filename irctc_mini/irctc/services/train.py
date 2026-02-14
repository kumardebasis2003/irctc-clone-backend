from django.db import transaction
from django.shortcuts import get_object_or_404
from irctc.models import train as train_models

class TrainService:
    """
    Service class for train-related operations (PostgreSQL only)
    """
    
    @staticmethod
    def search_trains(source, destination, date=None):
        """
        Search trains by source and destination
        
        Args:
            source (str): Source station name
            destination (str): Destination station name
            date (date, optional): Travel date
            
        Returns:
            QuerySet: Filtered train queryset
        """
        queryset = train_models.Train.objects.filter(
            source__iexact=source,
            destination__iexact=destination,
            active=True
        ).order_by('departure_time')
        
        return queryset
    
    @staticmethod
    def create_train(train_data):
        """
        Create a new train
        
        Args:
            train_data (dict): Train data dictionary
            
        Returns:
            train_models.Train: Created train instance
        """
        try:
            train = train_models.Train.objects.create(**train_data)
            return train
        except Exception as e:
            raise Exception(f"Failed to create train: {str(e)}")
    
    @staticmethod
    def update_train(train_id, train_data):
        """
        Update existing train
        
        Args:
            train_id (int): Train ID
            train_data (dict): Train data to update
            
        Returns:
            train_models.Train or None: Updated train instance or None
        """
        try:
            train = train_models.Train.objects.get(id=train_id)
            
            for key, value in train_data.items():
                setattr(train, key, value)
            
            train.save()
            return train
        except train_models.Train.DoesNotExist:
            return None
    
    @staticmethod
    def get_train_by_id(train_id):
        """
        Get train by ID
        
        Args:
            train_id (int): Train ID
            
        Returns:
            train_models.Train or None: Train instance or None if not found
        """
        try:
            return train_models.Train.objects.get(id=train_id, active=True)
        except train_models.Train.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_trains():
        """
        Get all active trains
        
        Returns:
            QuerySet: All active trains
        """
        return train_models.Train.objects.filter(active=True).order_by('departure_time')
    
    @staticmethod
    def deactivate_train(train_id):
        """
        Deactivate a train
        
        Args:
            train_id (int): Train ID
            
        Returns:
            bool: True if deactivated successfully, False otherwise
        """
        try:
            train = train_models.Train.objects.get(id=train_id)
            train.active = False
            train.save()
            return True
        except train_models.Train.DoesNotExist:
            return False
    
    @staticmethod
    def check_seat_availability(train_id, seats_requested):
        """
        Check if train has enough available seats
        
        Args:
            train_id (int): Train ID
            seats_requested (int): Number of seats requested
            
        Returns:
            bool: True if enough seats available, False otherwise
        """
        try:
            train = train_models.Train.objects.get(id=train_id, active=True)
            return train.has_available_seats(seats_requested)
        except train_models.Train.DoesNotExist:
            return False
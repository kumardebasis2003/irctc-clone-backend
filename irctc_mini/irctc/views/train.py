from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from irctc.services import train as train_services
from irctc.services import auth as auth_services
from irctc.serializers import train as train_serializers
from irctc.models import train as train_models

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users (main head users)
    """
    message = "Only admin users can perform this action."
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            auth_services.UserService.is_admin(request.user)
        )

class TrainSearchView(APIView):
    """
    Search trains between source and destination (No MongoDB logging)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Validate query parameters
        serializer = train_serializers.TrainSearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        
        source = serializer.validated_data['source']
        destination = serializer.validated_data['destination']
        limit = serializer.validated_data.get('limit', 10)
        offset = serializer.validated_data.get('offset', 0)
        
        # Search trains using service
        trains = train_services.TrainService.search_trains(source, destination)
        
        # Apply pagination manually
        total_count = trains.count()
        trains = trains[offset:offset + limit]
        
        # Serialize response
        train_serializer = train_serializers.TrainListSerializer(trains, many=True)
        
        response_data = {
            'count': total_count,
            'results': train_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class TrainCreateView(APIView):
    """
    Create a new train (Admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        serializer = train_serializers.TrainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            train = train_services.TrainService.create_train(serializer.validated_data)
            return Response(
                train_serializers.TrainSerializer(train).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class TrainUpdateView(APIView):
    """
    Update train details (Admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def put(self, request, id):
        try:
            train = train_models.Train.objects.get(id=id)
        except train_models.Train.DoesNotExist:
            return Response(
                {'error': 'Train not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = train_serializers.TrainSerializer(train, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_train = train_services.TrainService.update_train(id, serializer.validated_data)
        
        return Response(
            train_serializers.TrainSerializer(updated_train).data,
            status=status.HTTP_200_OK
        )

class TrainListView(APIView):
    """
    List all trains (Admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        trains = train_services.TrainService.get_all_trains()
        serializer = train_serializers.TrainListSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrainDetailView(APIView):
    """
    Get detailed information about a specific train
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, train_id):
        train = train_services.TrainService.get_train_by_id(train_id)
        
        if not train:
            return Response(
                {'error': 'Train not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            train_serializers.TrainSerializer(train).data,
            status=status.HTTP_200_OK
        )
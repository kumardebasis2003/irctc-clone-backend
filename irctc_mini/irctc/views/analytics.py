from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from irctc.services import analytics as analytics_services
from irctc.services import auth as auth_services
from irctc.serializers import analytics as analytics_serializers

class IsAdminUser(permissions.BasePermission):
    
    message = "Only admin users can access analytics data."
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            auth_services.UserService.is_admin(request.user)
        )

class TopRoutesAnalyticsView(APIView):
    
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get top routes from service
            top_routes = analytics_services.AnalyticsService.get_top_routes(limit=5)
            
            # Serialize route data
            serializer = analytics_serializers.TopRouteSerializer(top_routes, many=True)
            
            return Response({
                'top_routes': serializer.data,
                'total_searches_logged': analytics_services.SearchLog.objects.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserSearchAnalyticsView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            # Get user stats from service
            stats = analytics_services.AnalyticsService.get_user_search_stats(request.user.id)
            
            # Serialize stats
            serializer = analytics_serializers.UserSearchStatsSerializer(stats)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
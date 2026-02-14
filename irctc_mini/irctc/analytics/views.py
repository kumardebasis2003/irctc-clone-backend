from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from pymongo import MongoClient
from django.conf import settings
from collections import Counter

class TopRoutesAnalyticsView(APIView):
    """
    Get top 5 most searched routes from MongoDB logs
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            # Connect to MongoDB
            client = MongoClient(settings.MONGO_URI)
            db = client[settings.MONGO_DB_NAME]
            logs_collection = db['api_logs']
            
            # Get all search requests
            search_logs = logs_collection.find({
                'endpoint': '/api/trains/search/'
            })
            
            # Count route occurrences
            route_counts = Counter()
            for log in search_logs:
                params = log.get('params', {})
                source = params.get('source', '').lower()
                destination = params.get('destination', '').lower()
                
                if source and destination:
                    route = f"{source}-{destination}"
                    route_counts[route] += 1
            
            # Get top 5 routes
            top_routes = []
            for route, count in route_counts.most_common(5):
                source, destination = route.split('-')
                top_routes.append({
                    'source': source,
                    'destination': destination,
                    'search_count': count
                })
            
            return Response({
                'top_routes': top_routes
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
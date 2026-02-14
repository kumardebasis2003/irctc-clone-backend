from django.db.models import Count
from irctc.models import analytics as analytics_models

class AnalyticsService:
    
    @staticmethod
    def get_top_routes(limit=5):
        
        top_routes = analytics_models.SearchLog.objects.values(
            'source', 'destination'
        ).annotate(
            search_count=Count('id')
        ).order_by('-search_count')[:limit]
        
        return [
            {
                'source': route['source'],
                'destination': route['destination'],
                'search_count': route['search_count']
            }
            for route in top_routes
        ]
    
    @staticmethod
    def get_user_search_stats(user_id):
       
        # Get total searches by user
        total_searches = analytics_models.SearchLog.objects.filter(user_id=user_id).count()
        
        # Get unique routes searched
        unique_routes = analytics_models.SearchLog.objects.filter(
            user_id=user_id
        ).values('source', 'destination').distinct().count()
        
        # Get top 3 routes for this user
        top_routes = analytics_models.SearchLog.objects.filter(
            user_id=user_id
        ).values('source', 'destination').annotate(
            count=Count('id')
        ).order_by('-count')[:3]
        
        # Format top routes
        top_routes_list = [
            {
                'source': route['source'],
                'destination': route['destination'],
                'search_count': route['count']
            }
            for route in top_routes
        ]
        
        return {
            'total_searches': total_searches,
            'unique_routes_searched': unique_routes,
            'top_routes': top_routes_list
        }
    
    @staticmethod
    def get_search_logs(limit=50, offset=0):
        
        return analytics_models.SearchLog.objects.all()[offset:offset + limit]
    
    @staticmethod
    def get_total_search_count():
        
        return analytics_models.SearchLog.objects.count()
    
    @staticmethod
    def get_search_count_by_user(user_id):
        
        return analytics_models.SearchLog.objects.filter(user_id=user_id).count()
    
    @staticmethod
    def get_popular_sources(limit=10):
        
        sources = analytics_models.SearchLog.objects.values('source').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return [
            {
                'station': source['source'],
                'search_count': source['count']
            }
            for source in sources
        ]
    
    @staticmethod
    def get_popular_destinations(limit=10):
        
        destinations = analytics_models.SearchLog.objects.values('destination').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return [
            {
                'station': destination['destination'],
                'search_count': destination['count']
            }
            for destination in destinations
        ]
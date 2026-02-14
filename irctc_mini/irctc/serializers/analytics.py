from rest_framework import serializers

class TopRouteSerializer(serializers.Serializer):
    """
    Serializer for top searched routes
    
    Used in /api/analytics/top-routes/ response
    """
    source = serializers.CharField(
        max_length=100,
        help_text="Source station name"
    )
    destination = serializers.CharField(
        max_length=100,
        help_text="Destination station name"
    )
    search_count = serializers.IntegerField(
        min_value=0,
        help_text="Number of times this route was searched"
    )
    
    class Meta:
        fields = ['source', 'destination', 'search_count']

class UserSearchStatsSerializer(serializers.Serializer):
    """
    Serializer for user search statistics
    
    Used in /api/analytics/my-searches/ response
    """
    total_searches = serializers.IntegerField(
        min_value=0,
        help_text="Total number of searches performed by user"
    )
    unique_routes_searched = serializers.IntegerField(
        min_value=0,
        help_text="Number of unique routes searched by user"
    )
    top_routes = serializers.ListField(
        child=TopRouteSerializer(),
        help_text="Top 3 most searched routes by this user",
        required=False
    )
    
    class Meta:
        fields = ['total_searches', 'unique_routes_searched', 'top_routes']
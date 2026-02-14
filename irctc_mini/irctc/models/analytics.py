from django.db import models
from django.utils import timezone
from .auth import User

class SearchLog(models.Model):
    """
    PostgreSQL model to store train search queries for analytics
    Replaces MongoDB logging requirement
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='search_logs'
    )
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    search_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'search_logs'
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['search_time']),
        ]
        ordering = ['-search_time']
    
    def __str__(self):
        return f"{self.source} → {self.destination} at {self.search_time}"
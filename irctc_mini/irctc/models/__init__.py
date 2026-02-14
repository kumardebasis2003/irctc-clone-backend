"""
IRCTC Mini System - Models Package
"""

from .auth import (
    UserManager,
    User,
)

from .train import (
    Train,
)

from .booking import (
    Booking,
)

__all__ = [
    # User model
    'User',
    
    # Train model
    'Train',
    
    # Booking model
    'Booking',
]
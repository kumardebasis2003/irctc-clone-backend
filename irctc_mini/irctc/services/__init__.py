"""
IRCTC Mini System - Services Package
"""

# Import submodules to enable dotted imports
from . import auth
from . import train
from . import booking

# Also expose service classes directly for convenience
from .auth import UserService
from .train import TrainService
from .booking import BookingService

__all__ = [
    # Submodules (for dotted imports)
    'auth',
    'train',
    'booking',
    
    # Service classes (direct access)
    'UserService',
    'TrainService',
    'BookingService',
]
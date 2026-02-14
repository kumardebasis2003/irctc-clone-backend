"""
IRCTC Mini System - Views Package
"""

# Import submodules to enable dotted imports
from . import auth
from . import train
from . import booking

# Also expose view classes directly for convenience
from .auth import (
    RegisterView,
    LoginView,
    UserDetailView,
    TokenRefreshView,
    LogoutView,
)

from .train import (
    TrainSearchView,
    TrainCreateView,
    TrainUpdateView,
    TrainListView,
    #TrainDetailView,
)

from .booking import (
    BookingCreateView,
    UserBookingsView,
    #BookingDetailView,
    BookingCancelView,
    #AllBookingsView,
)

__all__ = [
    # Submodules (for dotted imports)
    'auth',
    'train',
    'booking',
    
    # Auth views
    'RegisterView',
    'LoginView',
    'UserDetailView',
    'TokenRefreshView',
    'LogoutView',
    
    # Train views
    'TrainSearchView',
    'TrainCreateView',
    'TrainUpdateView',
    'TrainListView',
    'TrainDetailView',
    
    # Booking views
    'BookingCreateView',
    'UserBookingsView',
    'BookingDetailView',
    'BookingCancelView',
    'AllBookingsView',
]
"""
IRCTC Mini System - Models Package
"""

# Import submodules to enable dotted imports (e.g., from irctc.models import auth as auth_models)
from . import auth
from . import train
from . import booking
from . import analytics  # ← ADD THIS LINE

# Import models and managers
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

from .analytics import (  # ← ADD THIS BLOCK
    SearchLog,
)

__all__ = [
    # Submodules (for dotted imports)
    'auth',
    'train',
    'booking',
    'analytics',  # ← ADD THIS LINE
    
    # Managers
    'UserManager',
    
    # Models
    'User',
    'Train',
    'Booking',
    'SearchLog',  # ← ADD THIS LINE
]
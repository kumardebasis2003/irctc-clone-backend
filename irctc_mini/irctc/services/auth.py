from ..models.auth import User

class UserService:
    @staticmethod
    def create_user(email, name, password):
        """
        Create a new user
        """
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def is_admin(user):
        """
        Check if user is admin
        """
        return user.is_admin
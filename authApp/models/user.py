from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Methods:
        - create_user(username, password, **extra_fields): Creates and saves a regular user.
        - create_superuser(username, password, **extra_fields): Creates and saves a superuser with admin permissions.
        - get_by_natural_key(username): Retrieves a user by their username.
    """
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and returns a user with the given username and password.
        
        Args:
            username (str): The username of the new user.
            password (str, optional): The password for the new user. Defaults to None.
            **extra_fields: Additional fields for the user model.

        Raises:
            ValueError: If the username is not provided.

        Returns:
            User: The created user instance.
        """
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given username and password.

        Superusers have admin permissions (`is_staff=True`, `is_superuser=True`).
        
        Args:
            username (str): The username of the new superuser.
            password (str, optional): The password for the new superuser. Defaults to None.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.

    Attributes:
        - _id (ObjectIdField): Primary key using MongoDB's ObjectId.
        - username (CharField): Unique username (max 15 characters).
        - is_active (BooleanField): Indicates if the user is active.

    Authentication:
        - USERNAME_FIELD: Defines 'username' as the unique identifier for authentication.
        - REQUIRED_FIELDS: Additional required fields (empty in this case).
    
    Meta:
        - managed = False: Indicates that Django should not manage this model in migrations.
        - db_table = "authApp_user": Sets the table name in the database.
    """
    _id = models.ObjectIdField(primary_key=True) 
    username = models.CharField('Username', max_length=15, unique=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False 
        db_table = "authApp_user"
        
    def __str__(self):
        return self.username
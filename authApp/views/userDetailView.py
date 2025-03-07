from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
from authApp.models.user import User
from authApp.serializers.userSerializer import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from bson import ObjectId

from utils.logger import LoggerHandler  # Necesario para trabajar con ObjectId


class UserDetailView(generics.RetrieveAPIView):
    """
    View to manage user details in a REST API.

    This view allows authenticated users to retrieve, create, and delete users via JWT authentication.

    Methods:
        - GET: Retrieves the list of all users if the JWT token is valid.
        - POST: Creates a new user if the username is not already in use.
        - DELETE: Deletes a specific user if the provided user ID is valid.

    Authentication:
        Uses JWT authentication to validate requests. If the token is missing or invalid, 
        a 401 (Unauthorized) response is returned.

    Exceptions:
        - If the token is invalid or expired, a 401 (Unauthorized) response is returned.
        - If the requested user does not exist, a 404 (Not Found) response is returned.
        - If the username is already in use during user creation, a 400 (Bad Request) response is returned.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    logger = LoggerHandler().get_logger()
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
 
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
   
        try:
            token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)  # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
          

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)

            inverter_data = User.objects.all()
            serializer = UserSerializer(inverter_data, many=True)
            return Response(serializer.data)

        except Exception as ex:
            self.logger.warning(f"Invalid token {ex}")
            return Response({'detail': 'Invalid token', 'error': str(ex)}, status=status.HTTP_401_UNAUTHORIZED)


    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization')
 
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
   
        try:
            token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)  # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
          


            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                if User.objects.filter(username=request.data['username']).exists():
                    return Response(
                        {"status": "error", "message": "El nombre de usuario ya está en uso."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                User.objects.create_user(username=request.data['username'], password=request.data['password'])

                return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response({"detail": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        auth_header = request.headers.get('Authorization')

     
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
   
        try:
            token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)  # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
          

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(_id=ObjectId(user_id))  # Usa ObjectId para convertir la cadena en el formato correcto
            user.delete()  
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        except User.DoesNotExist:

            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
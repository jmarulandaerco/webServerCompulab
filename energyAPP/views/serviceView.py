from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
from authApp.models.user import User
from authApp.serializers.userSerializer import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from bson import ObjectId

from utils import Menu  # Necesario para trabajar con ObjectId


class StartView(generics.RetrieveAPIView):
    """
    Starts the system service via Menu.start_service().

    GET:
    - Requires Bearer token authentication.
    - Verifies the user ID from the token matches the authenticated user.
    - Calls the method to start the system service.
    
    Responses:
    - 200 OK: {"message": "Sistema reiniciado"} if started successfully.
    - 200 OK: {"message": "Error empezando el computador"} if starting fails.
    - 401 Unauthorized: If token is missing, invalid, or user mismatched.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({'detail': 'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

            token = auth_header.split(' ')[1]

            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
            valid_data = token_backend.decode(token, verify=False)

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)

            started = Menu()
            start = started.start_service()
            if start == True:
                return Response({'message': 'Sistema reiniciado'})
            else:

                return Response({'message': 'Error empezando el computador'})

        except Exception as e:

            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class StopView(generics.RetrieveAPIView):
    """
    Stops the system service via Menu.stop_service().

    GET:
    - Requires Bearer token authentication.
    - Verifies the user ID from the token matches the authenticated user.
    - Calls the method to stop the system service.

    Responses:
    - 200 OK: {"message": "Parando sistema"} if stopped successfully.
    - 200 OK: {"message": "Servicio FW_main esta parado"} if already stopped.
    - 401 Unauthorized: If token is missing, invalid, or user mismatched.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
            valid_data = token_backend.decode(token, verify=False)

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Inautorizada petición'}, status=status.HTTP_401_UNAUTHORIZED)

            stopper = Menu()
            stop = stopper.stop_service()
            if stop == True:
                return Response({'message': 'Parando sistema'})
            else:

                return Response({'message': 'Servicio FW_main esta parado'})

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class Reboot(generics.RetrieveAPIView):
    """
    Reboots the system via Menu.reboot().

    GET:
    - Requires Bearer token authentication.
    - Verifies the user ID from the token matches the authenticated user.
    - Calls the method to reboot the system.

    Responses:
    - 200 OK: {"message": "Sistema reiniciado"} if rebooted successfully.
    - 200 OK: {"message": "Error reiniciando el pc"} if rebooting fails.
    - 401 Unauthorized: If token is missing, invalid, or user mismatched.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
            valid_data = token_backend.decode(token, verify=False)

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Petición inautorizada'}, status=status.HTTP_401_UNAUTHORIZED)

            stopper = Menu()
            stop = stopper.reboot()
            if stop == True:
                return Response({'message': 'Sistema reiniciado'})
            else:

                return Response({'message': 'Error reiniciando el pc'})

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class StatusService(generics.RetrieveAPIView):
    """
    Checks the status of the system service via Menu.check_service_status().

    GET:
    - No authentication required (unless added manually).
    - Calls method to check if the service is active or inactive.

    Responses:
    - 200 OK: {"active": True} if the service is running.
    - 200 OK: {"active": False} if the service is not running.
    - 401 Unauthorized: If token is required and invalid.
    """
    def get(self, request, *args, **kwargs):

        try:

            statusService = Menu()
            status_value = statusService.check_service_status()
            if status_value == True:
                return Response({'active': True})
            elif status_value == False:

                return Response({'active': False})
            else:
                return Response({'active': True})

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

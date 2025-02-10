from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
from authApp.models.user import User
from authApp.serializers.userSerializer import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from bson import ObjectId  # Necesario para trabajar con ObjectId


class RebootView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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

            
            return Response({'message':'Reiniciando Sistema'})

        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

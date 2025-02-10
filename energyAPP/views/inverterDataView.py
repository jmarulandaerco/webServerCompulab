
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from energyAPP.models import InverterData
from energyAPP.serializers import InverterDataSerializer

class InverterDataView(APIView):
    # authentication_classes = [JWTAuthentication]  # Usa JWTAuthentication
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 1️⃣ Obtener el encabezado 'Authorization'
        auth_header = request.headers.get('Authorization')
        print("Hola")
        print(auth_header)

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        # 2️⃣ Extraer el token (lo que viene después de 'Bearer ')
        token = auth_header.split(' ')[1]
   
        try:
            # 3️⃣ Decodificar el token manualmente
            token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)  # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
          

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)

            # 5️⃣ Obtener y serializar los datos
            inverter_data = InverterData.objects.all()
            serializer = InverterDataSerializer(inverter_data, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args, **kwargs):
         # 1️⃣ Obtener el encabezado 'Authorization'
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        # 2️⃣ Extraer el token (lo que viene después de 'Bearer ')
        token = auth_header.split(' ')[1]
        try:
            token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)  # ⚠️ `verify=False` para pruebas, usa `verify=True` en producción
          

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Unauthorized Request'}, status=status.HTTP_401_UNAUTHORIZED)

            InverterData.objects.all().delete()
            return Response({'detail': 'All records deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

            
        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        
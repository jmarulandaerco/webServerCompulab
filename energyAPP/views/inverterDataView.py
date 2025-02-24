
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from energyAPP.models import InverterData
from energyAPP.serializers import InverterDataSerializer
from pymongo import MongoClient

class InverterDataView(APIView):

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

class InverterView(View):
    def get(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        
        inverters_collection = db['inverters']
        
        inverters_data = list(inverters_collection.find().sort('_id', -1).limit(20))
        
        for inverter in inverters_data:
            inverter['_id'] = str(inverter['_id'])
        print(inverters_data)
        return render(request, 'home/content/databaseView.html', {'datos': inverters_data})
    
    
class InverterApiView(APIView):
    def get(self, request):
        try:
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
            db = client[settings.DATABASES['default']['NAME']]
            
            inverters_collection = db['inverters']
            
            inverters_data = list(inverters_collection.find())
            
            for inverter in inverters_data:
                inverter['_id'] = str(inverter['_id'])
            inverters_data
            
            df = pd.DataFrame(inverters_data)
            
            # Crear la respuesta de archivo Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="datos_inversores.xlsx"'
            
            # Escribir el DataFrame a un archivo Excel en la respuesta
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Datos Inversores")
            
        except Exception as ex:
            return HttpResponse(f"Error: {ex}")        
        return response

    
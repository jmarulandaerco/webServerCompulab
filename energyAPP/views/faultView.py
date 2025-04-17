from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework import status
from django.conf import settings
from pymongo import MongoClient
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse

from energyAPP.models import WeatherStationData
from energyAPP.models.faultModel import FaultData
from energyAPP.serializers import WeatherStationSerializer
from django.views import View
from django.core.paginator import Paginator

from energyAPP.serializers.faultSerializer import FaultDataSerializer



class FaultDataView(APIView):
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Petición inautorizada'}, status=status.HTTP_401_UNAUTHORIZED)

            fault = FaultData.objects.all()
            serializer = FaultDataSerializer(fault, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = token_backend.decode(token, verify=False)

            if str(valid_data['user_id']) != str(request.user):
                return Response({'detail': 'Petición inautorizado'}, status=status.HTTP_401_UNAUTHORIZED)

            FaultData.objects.all().delete()
            return Response({'detail': 'Datos elimidando correctamente'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class Fault(View):
    
    def get(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        fault_collection = db['faults']
        
        fault_data= list(fault_collection.find().sort('_id', -1))
        for weather_station in fault_data:
            weather_station['_id']=str(weather_station['_id'])
            
        per_page = int(request.GET.get('per_page', 10))
        page = int(request.GET.get('page', 1))
        
        paginator = Paginator(fault_data, per_page)
        data_paginader = paginator.get_page(page)
        
        return render(request, 'home/content/form/tables/databaseFault.html', {
            'datos': data_paginader,
            'per_page': per_page,
        })
        
class FaultApiView(APIView):
    
    def get(self, request):
        try:
            client = MongoClient(
                settings.DATABASES['default']['CLIENT']['host'])
            db = client[settings.DATABASES['default']['NAME']]

            fault_collection = db['faults']

            fault_data = list(fault_collection.find())

            for fault in fault_data:
                fault['_id'] = str(fault['_id'])
            fault_data

            df = pd.DataFrame(fault_data)

            # Crear la respuesta de archivo Excel
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="datos_fallos.xlsx"'

            # Escribir el DataFrame a un archivo Excel en la respuesta
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Datos fallos")

        except Exception as ex:
            return HttpResponse(f"Error: {ex}")
        return response
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
    """
    API View for retrieving and deleting fault data with JWT authentication.

    This view provides two methods:
    
    - GET: Returns a list of all fault data records in the database. It verifies the JWT 
      token provided in the 'Authorization' header. If the token is missing, invalid, or 
      does not match the authenticated user, it returns a 401 Unauthorized response.

    - DELETE: Deletes all fault data records from the database. It also requires a valid 
      JWT token and performs the same validation as the GET method. On successful deletion, 
      it returns a 204 No Content response.

    Both methods expect the JWT token in the following format:
        Authorization: Bearer <your_token>

    If an error occurs during token decoding or validation, a 401 Unauthorized response 
    is returned with the error details.
    """

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
    """
    Django view for displaying fault data from a MongoDB collection with pagination.

    This view connects to the MongoDB database configured in the Django settings,
    retrieves all documents from the 'faults' collection, sorts them in descending order 
    by their `_id`, and converts the `_id` field to a string for template rendering.

    The view supports pagination using `per_page` and `page` parameters from the query string:
        - `per_page`: Number of items per page (default: 10)
        - `page`: The current page number (default: 1)

    The paginated fault data is rendered in the 'databaseFault.html' template.

    Template context:
        - 'datos': Paginated fault data for the current page
        - 'per_page': Number of items per page

    Example URL:
        /faults/?page=2&per_page=20
    """
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
    """
    API View for exporting fault data stored in a MongoDB database.

    This endpoint handles GET requests and generates an Excel (.xlsx) file 
    containing the data retrieved from the 'faults' collection. The file is 
    returned as a downloadable response.

    Methods:
        get(request):
            Connects to MongoDB using the configuration defined in settings.DATABASES.
            Retrieves documents from the 'faults' collection, converts them into a 
            pandas DataFrame, and writes them to an Excel file attached to the HTTP response.
            
            If an error occurs, returns an HTTP response with the exception message.
    """
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

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
from django.core.paginator import Paginator


class InverterDataView(APIView):

    """
    API view to handle inverter data.

    Supported HTTP methods:
    - GET: Returns all inverter data records.
    - DELETE: Deletes all inverter data records.

    Authentication:
    - Requires Authorization header with a JWT token in Bearer format.
    - The token is decoded using SimpleJWT's TokenBackend.
    - The request is denied if the token is invalid or the user_id doesn't match.

    GET:
    - URL: /api/inverter-data/
    - Required headers: Authorization: Bearer <token>
    - Responses:
        * 200 OK: Returns a list of serialized InverterData objects.
        * 401 Unauthorized: Invalid token or unauthorized access.

    DELETE:
    - URL: /api/inverter-data/
    - Required headers: Authorization: Bearer <token>
    - Responses:
        * 204 No Content: All records successfully deleted.
        * 401 Unauthorized: Invalid token or unauthorized access.
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

            inverter_data = InverterData.objects.all()
            serializer = InverterDataSerializer(inverter_data, many=True)
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

            InverterData.objects.all().delete()
            return Response({'detail': 'Datos elimidando correctamente'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'detail': 'Token invalido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)




class InverterView(View):
    """
    Django view for displaying inverter data from a MongoDB collection.

    GET:
    - Connects to the MongoDB instance using Django settings.
    - Retrieves all documents from the 'inverters' collection, sorted by descending _id.
    - Converts ObjectId values to strings for template compatibility.
    - Supports pagination via GET parameters:
        * per_page (default: 10): Number of records per page.
        * page (default: 1): The page number to display.
    - Renders the 'home/content/databaseView.html' template with paginated data.

    Parameters:
    - per_page (int): Number of items per page, retrieved from GET parameters.
    - page (int): Current page number, retrieved from GET parameters.

    Template context:
    - datos: Paginated list of inverter documents.
    - per_page: Number of records per page used for rendering.
    """
    def get(self, request):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        inverters_collection = db['inverters']

        inverters_data = list(inverters_collection.find().sort('_id', -1))
        for inverter in inverters_data:
            inverter['_id'] = str(inverter['_id'])

        per_page = int(request.GET.get('per_page', 10))
        page = int(request.GET.get('page', 1))

        paginator = Paginator(inverters_data, per_page)
        data_paginader = paginator.get_page(page)

        return render(request, 'home/content/form/tables/databaseView.html', {
            'datos': data_paginader,
            'per_page': per_page,
        })



class InverterApiView(APIView):
    """
    API view that exports inverter data from MongoDB as an Excel (.xlsx) file.

    GET:
    - Connects to the MongoDB database using Django settings.
    - Fetches all documents from the 'inverters' collection.
    - Converts MongoDB ObjectId (_id) to string for compatibility.
    - Loads the data into a pandas DataFrame.
    - Generates an Excel file with the data and sends it as an HTTP response.

    Response:
    - Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    - Content-Disposition: attachment; filename="datos_inversores.xlsx"
    - Returns the Excel file containing all inverter records.

    Error Handling:
    - Returns a plain text HTTP response with the error message if any exception occurs.
    """
    def get(self, request):
        try:
            client = MongoClient(
                settings.DATABASES['default']['CLIENT']['host'])
            db = client[settings.DATABASES['default']['NAME']]

            inverters_collection = db['inverters']

            inverters_data = list(inverters_collection.find())

            for inverter in inverters_data:
                inverter['_id'] = str(inverter['_id'])
            inverters_data

            df = pd.DataFrame(inverters_data)

            # Crear la respuesta de archivo Excel
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="datos_inversores.xlsx"'

            # Escribir el DataFrame a un archivo Excel en la respuesta
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Datos Inversores")

        except Exception as ex:
            return HttpResponse(f"Error: {ex}")
        return response

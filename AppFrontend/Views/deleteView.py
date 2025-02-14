from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pymongo import MongoClient
from authApp.models.user import User
from utils.menu import Menu  # Importar modelos después de django.setup()


class DeleteCollectionView(APIView):
    def delete(self, request):
        try:
            # Conectar a MongoDB
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
            db = client[settings.DATABASES['default']['NAME']]

            # Eliminar todas las colecciones
            for collection_name in db.list_collection_names():
                db[collection_name].drop()
            
            User.objects.create_user(username="erco_to", password="3rc04dm1n#t0")
            User.objects.create_user(username="erco_config", password="3rc04dm1n#t0")

            return JsonResponse({"status": "success", "message": "Todas las colecciones han sido eliminadas."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

class DeleteLog(APIView):
    def delete(self,request):
        try:
            menu = Menu()
            menu.delete_log()
            JsonResponse({"message":"Logs eliminados"})
        except Exception as e:
            return JsonResponse({"message":"Error al eliminar"}, status=400)
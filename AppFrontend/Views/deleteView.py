import os
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pymongo import MongoClient
from authApp.models.user import User
from utils.menu import Menu  

menu = Menu()

class DeleteCollectionView(APIView):
    """
    A view to delete all collections from the MongoDB database and create two default users.

    Methods:
        delete: Connects to the MongoDB database, deletes all collections, and creates 
                two default users with predefined usernames and passwords.
    """
    def delete(self, request):
        try:
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
            db = client[settings.DATABASES['default']['NAME']]

           
            for collection_name in db.list_collection_names():
                db[collection_name].delete_many({})
            load_dotenv()
            passkey=os.getenv("PASS")
            if "#" not in passkey:
                passkey += "#t0"
            User.objects.create_user(username="erco_to", password=passkey)
            User.objects.create_user(username="erco_config", password=passkey)

            return JsonResponse({"status": "success", "message": "All collections have been deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

class DeleteLog(APIView):
    """
    A view to delete logs through the `Menu` utility class.

    Methods:
        delete: Deletes logs using the `Menu.delete_log()` method.
    """
    def delete(self,request):
        try:
            menu.delete_log()
            return JsonResponse({"message":"Logs deleted. Remember to stop and start the service if they do not exist. "},status=200)
        except Exception as e:
            return JsonResponse({"message":"Error when deleting"}, status=400)
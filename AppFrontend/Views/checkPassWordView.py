import json
from django.http import JsonResponse
from django.views import View
from utils.passwordUser import DataBaseMenu
from utils.menu import Menu


class CheckPassword(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Datos inválidos: uno o mas registros contiene datos invalidos o nulos"}, status=400)
                        
            
            password = data.get("password")
            confirm_password = data.get("confirmPassword")

            if not password or not confirm_password:
                return JsonResponse({"error": "Se requieren ambos campos"}, status=400)

            if password != confirm_password:
                return JsonResponse({"error": "Las contraseñas no coinciden"}, status=400)

            passwordDatabase = DataBaseMenu()
            if not passwordDatabase.check_password(password): 
                return JsonResponse({"error": "La contraseña ingresada no es válida"}, status=400)

            return JsonResponse({"message": "Las contraseñas coinciden"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)
        

class ChangePassword(View):
    def put(self, request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Datos inválidos: uno o mas registros contiene datos invalidos o nulos"}, status=400)
            
            
            password = data.get("actualPassword")
            new_password = data.get("newPassword")
            
            if not password or not new_password:
                return JsonResponse({"error": "Se requieren ambos campos"}, status=400)

        
            passwordDatabase = DataBaseMenu()
            if not passwordDatabase.check_password(password):  
                return JsonResponse({"error": "La contraseña ingresada no es válida"}, status=400)
            
            menu = Menu()
            change = menu.change_user_password(new_password)
            if change:
                return JsonResponse({"message":"Contraseña actualizada."})
            else:
                return JsonResponse({"message":"Contraseña no actualizada."},status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

import json
import os
from django.http import JsonResponse
from django.views import View
from dotenv import load_dotenv
from utils.passwordUser import DataBaseMenu
from utils.menu import Menu


class CheckPassword(View):
    """
    API View to check if the provided passwords match and if the password is valid.

    This view handles POST requests to verify if the 'password' and 'confirmPassword' fields match 
    and if the provided password is valid according to the password database.

    Methods:
    -------
    post(request)
        Handles POST requests to check if the passwords match and if the password is valid.
        Returns a JSON response with a message indicating success or error.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Datos invalidos: uno o más registros contienen datos no válidos o nulos."}, status=400)

            password = data.get("password")
            confirm_password = data.get("confirmPassword")

            if not password or not confirm_password:
                return JsonResponse({"message": "Ambos datos son requeridos"}, status=400)

            if password != confirm_password:
                return JsonResponse({"message": "Las contraseñas no son iguales"}, status=400)

            passwordDatabase = DataBaseMenu()
            if not passwordDatabase.check_password(password):
                
                return JsonResponse({"message": f"La contraseña ingresada no es valida"}, status=400)

            return JsonResponse({"message": "Contraseñas Correcta"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Formato Json invalido"}, status=400)


class ChangePassword(View):
    """
    API View to change the user's password.

    This view handles PUT requests to update the user's password. It checks if the current password is valid, 
    and if so, updates the password to the new one.

    Methods:
    -------
    put(request)
        Handles PUT requests to update the user's password after validating the current password.
        Returns a JSON response indicating success or failure of the update.
    """

    def put(self, request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Datos invalidos: uno o más registros contienen datos no válidos o nulos"}, status=400)

            password = data.get("actualPassword")
            new_password = data.get("newPassword")
            reply_new_password=data.get("replyNewPassword")
            
            if new_password != reply_new_password:
                return JsonResponse({"message":"Las contraseñas son diferentes"},status=400)
            if new_password == "" or reply_new_password=="":
                return JsonResponse({"message":"Los campos estan vacios"},status=400)
            if not password or not new_password:
                return JsonResponse({"message": "Ambos campos son requeridos"}, status=400)

            passwordDatabase = DataBaseMenu()
            if not passwordDatabase.check_password_erco_config(password):
                return JsonResponse({"message": "La contraseña actual es invalida"}, status=400)

            menu = Menu()
            change = menu.change_user_password(new_password)
            if change:
                menu.update_user_password("erco_config",new_password)
                return JsonResponse({"message": "Contraseña actualizada."})
            else:
                return JsonResponse({"message": "Contraseña no actualizada"}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": "Formato JSON inválido"}, status=400)

import json
import configparser
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from utils.configfiles import ConfigFilePaths

# Obtiene la lista de rutas desde tu clase utilitaria
cf = ConfigFilePaths()
list_path_menu = cf.to_list()  # Asumimos que aquí ya tienes la ruta correcta
# Usaremos la posición 7 (índice 6)
INIT_PATH = list_path_menu[6]


@method_decorator(csrf_exempt, name="dispatch")
class SaveInitView(View):
    """
    Recibe los datos de JS y los guarda en el archivo .init (posición 7 de list_path_menu).
    """

    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON inválido")

        fields = payload.get("fields")
        if not isinstance(fields, list):
            return HttpResponseBadRequest("'fields' debe ser lista.")

        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str  # Preserva nombres tal cual

        for field in fields:
            group = field.get("group")
            addr = field.get("address")
            val = field.get("value")

            if not group or addr is None or val is None:
                continue

            # Validación numérica básica
            try:
                addr = int(addr)
                val = float(val)
            except (TypeError, ValueError):
                continue

            # Agregar sección si no existe
            if group not in config:
                config[group] = {}

            config[group]["address"] = str(addr)
            config[group]["value"] = str(val)

        if not config.sections():
            return HttpResponseBadRequest("No hay campos válidos para guardar.")

        try:
            with open(INIT_PATH, "w") as configfile:
                config.write(configfile)
        except Exception as e:
            return HttpResponseBadRequest(f"No se pudo escribir en {INIT_PATH}: {e}")

        return JsonResponse({
            "ok": True,
            "message": f"Datos guardados en {INIT_PATH}",
            "path": INIT_PATH,
            "sections": config.sections()
        })

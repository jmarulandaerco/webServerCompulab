import json
import configparser
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from utils.configfiles import ConfigFilePaths

cf = ConfigFilePaths()
list_path_menu = cf.to_list()
INIT_PATH = list_path_menu[7]  # posición 7

@method_decorator(csrf_exempt, name="dispatch")
class SaveInitView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception as exc:
            return HttpResponseBadRequest(f"JSON inválido: {exc}")

        fields = payload.get("fields")
        if not isinstance(fields, list):
            return HttpResponseBadRequest("'fields' debe ser lista.")

        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str

        for field in fields:
            group = field.get("group")
            addr = field.get("address")
            val = field.get("value")

            if not group or addr is None or val is None:
                continue

            try:
                addr = int(addr)
                val = float(val)
            except (TypeError, ValueError):
                continue

            if group not in config:
                config[group] = {}

            config[group]["address"] = str(addr)
            config[group]["value"] = str(val)

        if not config.sections():
            return HttpResponseBadRequest("No hay campos válidos para guardar.")

        try:
            with open(INIT_PATH, "w") as fh:
                config.write(fh)
        except Exception as exc:
            return HttpResponseBadRequest(f"No se pudo escribir en {INIT_PATH}: {exc}")

        return JsonResponse({
            "ok": True,
            "message": f"Datos guardados en {INIT_PATH}",
            "path": INIT_PATH,
            "sections": config.sections(),
        })

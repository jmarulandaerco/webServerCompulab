# views_bess.py
import json
import configparser

from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

from utils.configfiles import ConfigFilePaths


# Localiza el archivo bess_battery.init
cf = ConfigFilePaths()
list_path_menu = cf.to_list()
INIT_PATH = list_path_menu[7]   # Ajusta si cambia la posición


@method_decorator(csrf_exempt, name="dispatch")   # quítalo si quieres CSRF
class BessTcpWriteView(View):
    """
    POST  -> Recibe parámetros TCP y escribe los valores definidos en bess_battery.init al dispositivo Modbus.
    GET   -> (Opcional) Devuelve vista previa: contenido del archivo .init (sin escribir).

    Espera JSON POST:
    {
      "host": "10.6.20.10",
      "port": 502,
      "attempts": 3,
      "timeout": 1.0,
      "slave": 1,
      "function": 6,       # 6 = single write loop; 10 = write multiple
      "preview": false     # si true, sólo lee y devuelve; no escribe
    }
    """
    # -------- GET: sólo devuelve los datos del archivo .init --------
    def get(self, request):
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        try:
            config.read(INIT_PATH)
        except Exception as exc:
            return JsonResponse({"ok": False, "message": f"No se pudo leer {INIT_PATH}: {exc}", "fields": []}, status=500)

        fields = []
        for section in config.sections():
            fields.append({
                "group": section,
                "address": config.get(section, "address", fallback=None),
                "value": config.get(section, "value", fallback=None),
            })

        return JsonResponse({"ok": True, "fields": fields})

    # -------- POST: escribir por Modbus TCP --------
    def post(self, request):
        # Parse JSON
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception as exc:
            return HttpResponseBadRequest(f"JSON inválido: {exc}")

        host     = payload.get("host")
        port     = payload.get("port", 502)
        attempts = payload.get("attempts", 1)
        timeout  = payload.get("timeout", 1)
        slave    = payload.get("slave", 1)
        func     = payload.get("function", 6)
        preview  = payload.get("preview", False)

        # Validaciones mínimas
        if not host:
            return HttpResponseBadRequest("Host requerido.")
        try: port = int(port)
        except Exception: return HttpResponseBadRequest("Puerto inválido.")
        try: attempts = int(attempts)
        except Exception: attempts = 1
        try: timeout = float(timeout)
        except Exception: timeout = 1.0
        try: slave = int(slave)
        except Exception: slave = 1
        try: func = int(func)
        except Exception: func = 6

        # Leer archivo init
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        try:
            config.read(INIT_PATH)
        except Exception as exc:
            return HttpResponseBadRequest(f"No se pudo leer {INIT_PATH}: {exc}")

        regs = []
        for section in config.sections():
            try:
                addr = int(config.get(section, "address"))
                val  = float(config.get(section, "value"))
            except Exception:
                continue
            regs.append((section, addr, val))

        if not regs:
            return HttpResponseBadRequest("No hay campos válidos en el archivo init.")

        # Si sólo vista previa
        if preview:
            preview_rows = [
                {"group": s, "address": a, "value": v} for (s, a, v) in regs
            ]
            return JsonResponse({
                "ok": True,
                "message": "Vista previa: no se envió nada por Modbus (preview=true).",
                "wrote": preview_rows,
            })

        # Conectar y escribir
        client = ModbusTcpClient(host=host, port=port, timeout=timeout)
        if not client.connect():
            return HttpResponseBadRequest(f"No se pudo conectar a {host}:{port}.")

        results = []
        try:
            if func == 10 and len(regs) > 1:
                # ---------- FUNCIÓN 16 (0x10) ESCRIBIR MÚLTIPLES ----------
                # Ordenamos por address
                regs_sorted = sorted(regs, key=lambda r: r[1])
                base_addr = regs_sorted[0][1]
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                last_addr = base_addr

                # Para reporte:
                sec_report = []

                for section, addr, val in regs_sorted:
                    # Rellenar huecos con 0 si addresses no contiguos
                    while last_addr < addr:
                        builder.add_16bit_uint(0)
                        last_addr += 1
                    builder.add_16bit_uint(int(val))
                    sec_report.append((section, addr, val))
                    last_addr = addr + 1

                payload_regs = builder.to_registers()

                rr = client.write_registers(base_addr, payload_regs, slave=slave)
                ok = not rr.isError()
                err_str = None if ok else str(rr)

                for section, addr, val in sec_report:
                    results.append({
                        "group": section,
                        "address": addr,
                        "value": val,
                        "ok": ok,
                        "error": err_str,
                    })
            else:
                # ---------- FUNCIÓN 6 (0x06) ESCRIBIR UNO POR UNO ----------
                for section, addr, val in regs:
                    write_val = int(val)  # Ajusta si tienes factor escala
                    success = False
                    error_msg = None

                    for _ in range(attempts):
                        rr = client.write_register(addr, write_val, slave=slave)
                        if not rr.isError():
                            success = True
                            break
                        error_msg = str(rr)

                    results.append({
                        "group": section,
                        "address": addr,
                        "value": val,
                        "ok": success,
                        "error": error_msg,
                    })
        finally:
            client.close()

        return JsonResponse({
            "ok": True,
            "message": f"Escritura Modbus completada a {host}:{port}.",
            "wrote": results,
        })

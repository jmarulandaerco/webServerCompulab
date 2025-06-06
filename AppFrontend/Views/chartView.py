import configparser
import json
import os
import subprocess
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from utils.configfiles import ConfigFilePaths
from utils.menu import Menu
from utils.menu_single_device import SingleDeviceRead

class chartRAM(APIView):

    def get(self, request):
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            exit = result.stdout

            # Parsear salida para extraer datos de Mem y Swap
            lines = exit.splitlines()

            # Buscamos la línea que empieza con "Mem:" y "Swap:"
            memory_line = next((l for l in lines if l.startswith('Mem:')), None)
            swap_line= next((l for l in lines if l.startswith('Swap:')), None)

            # Separar columnas, la salida está tipo:
            # Mem:  total used free shared buff/cache available
            # Split por espacios filtrando vacíos
            mem_vals = memory_line.split()
            swap_vals = swap_line.split()

            data = {
                'memoria': {
                    'total': mem_vals[1],
                    'usada': mem_vals[2],
                    'libre': mem_vals[3],
                    'compartida': mem_vals[4],
                    'buffer_cache': mem_vals[5],
                    'disponible': mem_vals[6],
                },
                'swap': {
                    'total': swap_vals[1],
                    'usada': swap_vals[2],
                    'libre': swap_vals[3],
                }
            }

            return JsonResponse(data)


        except json.JSONDecodeError:
            return JsonResponse({"message": "Error parciando los datos en el JSON"}, status=400)
        except Exception as ex:
            return JsonResponse({"message": f"Error actualizando los datos: {ex}"}, status=400)

class TopCPUProcesses(APIView):
    def get(self, request):
        try:
            # Ejecutar comando
            cmd = "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | grep -v -E 'sshd|ps' | head -n 5"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()

            # Separar líneas
            lines = output.splitlines()

            # La primera línea es encabezado: PID COMMAND %CPU %MEM
            # parsear el resto de líneas
            processes = []
            for line in lines[1:]:
                # Separar por espacios múltiples
                parts = line.split()
                if len(parts) == 4:
                    pid, command, cpu, mem = parts
                    processes.append({
                        "pid": int(pid),
                        "command": command,
                        "cpu": float(cpu),
                        "mem": float(mem),
                    })

            data = {
                "top_processes": processes
            }

            return JsonResponse(data)

        except Exception as ex:
            return JsonResponse({"message": f"Error obteniendo los datos: {ex}"}, status=400)
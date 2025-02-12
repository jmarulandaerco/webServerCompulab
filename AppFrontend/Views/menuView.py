from django.http import JsonResponse
from django.views import View

class MeasureView(View):
    def get(self, request):
        sample_data = {
            "zone": "UTC-5",
            "modbus": "9600",
            "start": "08:00",
            "stop": "18:00",
        }
        return JsonResponse(sample_data)

class FormDataServer(View):
    def get(self, request):
        sample_data = {
            "Server": "Neu plus",  # Puede ser "Telemetry", "Neu plus" o "All services"
            "neu_plus": "123456",
            "telemetry": "ABCDEF",
            "mqtt": "1000",
            "storage": "5000",
        }
        return JsonResponse(sample_data)
    
class FormDataModes(View):
    def get(self, request):
        sample_data = {
             "mode": "Automatic",            # Valor de ejemplo para el modo
            "limitation": "Yes",            # Opciones: "Yes" o "No"
            "compensation": "Yes",           # Opciones: "Yes" o "No"
            "sampling_limitation": "5s",    # Ejemplo: 5 segundos
            "sampling_compensation": "10s", # Ejemplo: 10 segundos
        }
        return JsonResponse(sample_data)

class FormDataSettingDataBase(View):
    def get(self,request):
        sample_data = {
            "day":"30",
            "await":"2",
        }
        return JsonResponse(sample_data)
    
class FormDataSettingInterface(View):
    def get(self,request):
        sample_data = {
            "interface":"wlan0",
            "connection":"Red-Onomondo",
        }
        return JsonResponse(sample_data)

class FormDataLimitation(View):
    def get(self,request):
        sample_data= {
            "limitation":"Yes",
            "meter_ids":"11",
            "inverter_ids":"1",
            "porcentage":"0.02",
            "grid_min":"5",
            "grid_max":"10",
            "inverter_min":"0",
            "inverterMax":"1000",

        }
        return JsonResponse(sample_data)

class FormDataCompensation(View):
    def get(self,request):
        sample_data= {
            "reactive_power":"No",
            "meter_ids":"4.5",
            "smart_logger":"10",
            "high":"0.4",
            "low":"0.3",
            "reactive":"0",
            "active":"0",
            "time":"0.1",
            "factor":"0.91"

        }
        return JsonResponse(sample_data)
    


class FormDataBasePropierties(View):
    def get(self,request):
        sample_data= {
            "host":"localhost",
            "port":"27017",
            "name":"device_local_database",
            "timeout":"10",
            "date":"%Y-%m-%d %H:%M:%S"
            

        }
        return JsonResponse(sample_data)


from django.http import JsonResponse
from django.views import View

class FormModbusView(View):
    def get(self, request):
        sample_data = {
            "debug": "DEBUG",
            "attempts": "3",
            "timeout": "1",
        }
        return JsonResponse(sample_data)
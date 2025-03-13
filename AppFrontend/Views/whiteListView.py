import json
import subprocess
from django.http import JsonResponse
from rest_framework.views import APIView

from utils.logger import LoggerHandler
from utils.whitelist import WhiteList


# Colocar el self.logger
logger = LoggerHandler().get_logger()

"""
    Class that handles the removal of a modem from the whitelist using AT commands.

    Methods:
    - post: This method handles the POST request to remove a modem from the whitelist.
      It sends three AT commands to the device to check the status, clear the whitelist, and restart the device.
      Returns a JSON with the status of each operation.
    """


class DeleteWhiteList(APIView):

    def post(self, request):
        try:
            at_command_check = 'AT'
            at_command_clear = 'AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFFFFFFFFFFF"'
            at_command_restart = 'AT+CFUN=1,1'
            print("hola")
            data = json.loads(request.body)
            print(data)
            port = data.get("modemSelect")
            print(port)
            white_list = WhiteList(port, 115200)
            check = white_list.send_at_command(at_command_check)
            clear = white_list.send_at_command(at_command_clear)
            restart = white_list.send_at_command(at_command_restart)
            return JsonResponse({"message": f"status check: {str(check)}, status clear: {str(clear)}, status restart: {str(restart)}"}, status=200)

        except Exception as ex:
            logger.info("Error delete whitelist: " + str(ex))
            return JsonResponse({"message": str(ex)}, status=400)


    """
    Class to manage the modem service state.

    Methods:
    - post: This method handles the POST request to start or stop the modem service.
      Depending on the provided parameter, the modem service is either started or stopped.
      Returns a JSON with the operation status.
    """
class ModemManager(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            control = WhiteList()
            status = control.control_modem_service(
                bool(data.get("startManagerModemService")))
            print("Holaaaa")
            print(status)
            if status:
                if bool(data.get("startManagerModemService")):
                    return JsonResponse({"message": "Moden started correctly."}, status=200)

                return JsonResponse({"message": "Modem stopped correctly."}, status=200)

            return JsonResponse({"message": "Faille started or stoped the modem"}, status=400)
        except Exception as ex:
            print("Error muy malisimo")

            return JsonResponse({"message": str(ex)}, status=400)

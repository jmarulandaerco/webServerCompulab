import json
import subprocess
from django.http import JsonResponse
from rest_framework.views import APIView

from utils.logger import LoggerHandler
from utils.whitelist import WhiteList


##Colocar el self.logger
logger = LoggerHandler().get_logger()
    
class DeleteWhiteList(APIView):
    
    def post(self, request):
        try:
            at_command_check = 'AT'
            at_command_clear = 'AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFFFFFFFFFFF"'
            at_command_restart = 'AT+CFUN=1,1'

            data = json.loads(request.body)
            port = data.get("modemSelect")
            white_list=WhiteList(port,115200)
            check = white_list.send_at_command(at_command_check)
            clear = white_list.send_at_command(at_command_clear)
            restart = white_list.send_at_command(at_command_restart)
            JsonResponse({"message":f"status check: {check}, status clear{clear}, status restart {restart}"},200)
        
        except Exception as ex:
            logger.info("Error delete whitelist: "+ str(ex))
            return JsonResponse({"message": str(ex)}, status=400)

         
class ModemManager(APIView):
    def post(self,request):
        try:
            data=json.loads(request.body)
            control=WhiteList()
            status =control.control_modem_service()
            
            if status:            
                if bool(data.get("startManagerModemService")):
                    return JsonResponse({"message":"Moden started correctly."},200)

                return JsonResponse({"message":"Modem stopped correctly."},200)
            
            return JsonResponse({"message":"Faille started or stoped the modem"},400)
        except Exception as ex:
            return JsonResponse({"message":str(ex)})

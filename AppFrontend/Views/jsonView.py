import json
from django.http import HttpResponse
from django.db import connections
from rest_framework.views import APIView

class ListColections(APIView):
    def get(self, request):
        try:
            # Obtener la conexión a MongoDB desde Djongo
            db = connections['default']

            # Obtener todas las colecciones
            colecciones = db.cursor().db_conn.list_collection_names()

            # Obtener los datos de cada colección
            datos = {}
            for coleccion in colecciones:
                collection_ref = db.cursor().db_conn[coleccion]
                datos[coleccion] = list(collection_ref.find({}, {"_id": 0}))  # Excluir _id para evitar problemas de serialización

            # Convertir datos a JSON
            json_data = json.dumps({"colecciones": datos}, indent=4)

            # Crear la respuesta con el archivo TXT
            response = HttpResponse(json_data, content_type="text/plain")
            response["Content-Disposition"] = 'attachment; filename="colecciones.txt"'

            return response

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)

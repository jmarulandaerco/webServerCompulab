import json
from django.http import HttpResponse
from django.db import connections
from rest_framework.views import APIView
from datetime import datetime

class ListColections(APIView):
    def get(self, request):
        try:

            db = connections['default']

            collections = db.cursor().db_conn.list_collection_names()

            data = {}
            for collection in collections:
                if collection != 'authApp_user':
                    collection_ref = db.cursor().db_conn[collection]
                    data[collection] = list(collection_ref.find({}, {"_id": 0}))
            json_data = json.dumps({"collections": data}, indent=4, default=str)
            current_datetime = datetime.now()
            filename = current_datetime.strftime('collections_%Y-%m-%d_%H-%M-%S.txt')
            response = HttpResponse(json_data, content_type="text/plain")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)
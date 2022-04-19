from rest_framework.views import APIView
from core.models import Quotes
from datetime import datetime
from core.helpers import api_response
import time
class QuotesView(APIView):
    def get(self,request):
        tdy = datetime.today().date()
        qts = Quotes.objects.filter(display_date=tdy).first()
        if qts:
            data=[{
                '_id':qts.image_id,
                'image_uri':qts.image_uri,
                'download_uri':qts.download_uri,
            }]
            time.sleep(2)
            return api_response(200,"quote retrieved successfully",data)
        else:
            return api_response(400,"Sorry no quote updated today",[])
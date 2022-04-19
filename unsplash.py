import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quote_be.settings")
django.setup()

from core.models import Quotes
import requests
import json
import pandas as pd
import datetime

unsplash_api = "https://api.unsplash.com"
end_point = "search/photos/"
# page_number = 1
query = "motivational quotes"
client_id = "ce43uCX2tyx4kGKPJOqgOKQ5zZw-PUqgLYSrJmhri70"

def create_quote(page_number):
    url = f"{unsplash_api}/{end_point}?&page={page_number}&query={query}&client_id={client_id}&orientation=portrait"

    resp = requests.get(url)

    res = json.loads(resp.text)

    for item in res["results"]:
        _id = item['id']
        _url = item['urls']['raw']+"&w=750&dpr=2"
        _download = item['links']['download']
        if not Quotes.objects.filter(image_id=_id).exists():
            Quotes.objects.create(image_id=_id,image_uri=_url,download_uri=_download)
        else:
            pass

if __name__ == "__main__":
    print("populating")
    create_quote(5)
    print("done")




q= Quotes.objects.all()

last_dt_obj = q.filter(display_date__isnull=False).order_by('-display_date').first()

last_dt = datetime.datetime.now().date()

if last_dt_obj:
    last_dt = last_dt_obj.display_date + datetime.timedelta(days=1)

end_date = last_dt + datetime.timedelta(days=100)

dts = pd.date_range(start=last_dt,end=end_date).to_pydatetime().tolist()

for i, obj in enumerate(q.filter(display_date__isnull=True)):
    if not q.filter(display_date = dts[i]).exists():
        obj.display_date = dts[i]
        obj.save()
    else:
        pass
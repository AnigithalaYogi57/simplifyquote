from rest_framework.response import Response
import re
from core.models import User

def api_response(code, message, data):
    data = {
        "status": code,
        "message": message,
        "data": data,
    }
    response = Response(data=data, status=code)
    response["Cache-Control"] = "no-store"
    response["Pragma"] = "no-cache"
    return response


def generate_username(email):
    account_name = re.findall("[a-zA-Z0-9_.+-]+", email)
    val = "{0}".format(account_name[0]).lower()
    x = 0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}".format(val, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 1000000:
            raise Exception("Unable to create username , Name is super popular!")

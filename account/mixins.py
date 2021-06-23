import json
import urllib

from config import settings
from django.shortcuts import redirect


class CheckRecaptchaMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.check_recaptcha(request):
            return super().dispatch(request, *args, **kwargs)
            
        applicant_path = request.POST.get("applicant_path")
        dict_obj = {"type": "recaptcha_not_ok", "content": None}
        request.session["event"] = json.dumps(dict_obj)
        return redirect(applicant_path)

    def check_recaptcha(self, request):
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result["success"]:
            return True
        return False

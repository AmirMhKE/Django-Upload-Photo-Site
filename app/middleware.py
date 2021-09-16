from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from extensions.utils import get_apps_views, get_client_ip
from jdatetime import datetime, timedelta

from .models import Ip

User = get_user_model()


class RequestProcessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.save_request_count(request, view_func)

    @classmethod
    def save_request_count(cls, request, view_func):
        """
        This function save request count users in the database
        """
        user = None
        view_lists = get_apps_views()

        if view_func.__name__ in view_lists:
            cls.process_client_ip(request)

        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)

        # ? Count all requests
        if user and view_func.__name__ in view_lists:
            user.all_requests_count += 1
            user.save()

        # ? Count all download requests
        if user and view_func.__name__ == "DownloadView":
            user.requests_download_count += 1
            user.save()

    @classmethod
    def process_client_ip(cls, request):
        """
        This function save new ip address users in the database
        """
        ip_address = get_client_ip(request)

        obj = Ip.objects.get_or_create(ip_address=ip_address)[0]

        cls.check_excessive_requests(request, obj)

    @staticmethod
    def check_excessive_requests(request, obj):
        """
        This function can prevent DDOS attacks as much as possible
        """
        if not request.user.is_superuser:
            minus = datetime.now().timestamp() - obj.last_excessive_request_time.timestamp()
            block_time_seconds = randint(settings.MIN_BLOCK_TIME_EXCESSIVE_REQUESTS,
            settings.MAX_BLOCK_TIME_EXCESSIVE_REQUESTS)
            minimum_difference_float = settings.MINIMUM_DIFFERENCE_REQUESTS
            max_count = settings.MAX_COUNT_EXCESSIVE_REQUESTS
            
            if obj.excessive_requests_count < max_count:
                if not obj.excessive_requests_count:
                    obj.excessive_requests_count = 1
                    obj.last_excessive_request_time = datetime.now()
                    obj.save()
                elif minus < minimum_difference_float:
                    obj.excessive_requests_count += 1
                    obj.save()
                else:
                    obj.excessive_requests_count = 0
                    obj.save()

                # ? Save excessive count request user
                if obj.excessive_requests_count == max_count and request.user.is_authenticated:
                    user = User.objects.get(pk=request.user.pk)
                    user.excessive_requests_count += 1
                    user.save()
            else:
                difference_block_time = obj.last_excessive_request_time \
                + timedelta(seconds=block_time_seconds)

                if datetime.now().timestamp() < difference_block_time.timestamp():
                    diffrence = difference_block_time.timestamp() - datetime.now().timestamp()
                    message = " ".join(f"You have been blocked for {round(diffrence, 2)} \
                    seconds due to excessive requests!".split())
                    raise Http404(message)

                obj.excessive_requests_count = 0
                obj.save()

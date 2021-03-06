from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from extension.utils import get_apps_views, get_client_ip
from jdatetime import datetime, timedelta

from .models import Ip

User = get_user_model()


class RequestProcessMiddleware:
    minimum_difference_float = settings.MINIMUM_DIFFERENCE_REQUESTS
    max_count = settings.MAX_COUNT_EXCESSIVE_REQUESTS

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        not_found, internal_server_error = 404, 500
        response = self.get_response(request)
        header = response.headers

        try:
            if response.status_code in [not_found, internal_server_error] \
            and header["Content-Type"].split(";")[0] == "text/html":
                self.process_client_ip(request)
        except (KeyError, IndexError):
            pass

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.save_request_count(request, view_func)

    def save_request_count(self, request, view_func):
        """
        This function save request count users in the database
        """
        user = None
        view_lists = get_apps_views()

        if view_func.__name__ in view_lists:
            self.process_client_ip(request)

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

    def process_client_ip(self, request):
        """
        This function save new ip address users in the database
        """
        ip_address = get_client_ip(request)
        obj = Ip.objects.get_or_create(ip_address=ip_address)[0]
        self.check_excessive_requests(request, obj)

    def check_excessive_requests(self, request, obj):
        """
        This function can prevent DDOS attacks as much as possible
        """
        if not request.user.is_superuser:
            minus = datetime.now().timestamp() - obj.last_excessive_request_time.timestamp()

            if obj.excessive_requests_count < self.max_count:
                if minus < self.minimum_difference_float or not obj.excessive_requests_count:
                    obj.excessive_requests_count += 1
                    obj.last_excessive_request_time = datetime.now()
                    obj.save()
                else:
                    obj.excessive_requests_count = 0
                    obj.save()

                # ? Save excessive count request user
                if obj.excessive_requests_count == self.max_count and request.user.is_authenticated:
                    user = User.objects.get(pk=request.user.pk)
                    user.excessive_requests_count += 1
                    user.save()

                if obj.excessive_request_block_time is not None:
                    obj.excessive_request_block_time = None
                    obj.save() 
            else:
                if obj.excessive_request_block_time is None:
                    obj.excessive_request_block_time = randint(
                        settings.MIN_BLOCK_TIME_EXCESSIVE_REQUESTS,
                        settings.MAX_BLOCK_TIME_EXCESSIVE_REQUESTS
                    )
                    obj.save()

                difference_block_time = obj.last_excessive_request_time \
                + timedelta(seconds=obj.excessive_request_block_time)

                if datetime.now().timestamp() < difference_block_time.timestamp():
                    diffrence = difference_block_time.timestamp() - datetime.now().timestamp()
                    message = " ".join(f"You have been blocked for {round(diffrence, 2)} \
                    seconds due to excessive requests!".split())
                    raise Http404(message)

                obj.excessive_requests_count = 0
                obj.save()

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.http import Http404

from .models import Ip

User = get_user_model()

class RequestProcessMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        return response

    # ? Save request count user in database
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = None
        view_lists = ["PostList", "PostDetail", "PublisherList", "CategoryList", "SearchList", 
        "DownloadView", "LikeView", "StatisticsView"]

        if view_func.__name__ in view_lists:
            self.process_client_ip(request)

        if request.user.is_authenticated:
            username = request.user.username
            email = request.user.email
            user = User.objects.filter(username=username, email=email)[0]

        # ? Count all requests
        if user and view_func.__name__ in view_lists:
            user.all_requests_count += 1

            user.save()

        # ? Count all search requests
        if user and view_func.__name__ == "SearchList":
            user.requests_search_count += 1

            user.save()

        # ? Count all download requests
        if user and view_func.__name__ == "DownloadView":
            user.requests_download_count += 1

            user.save()

    def process_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        query = Ip.objects.filter(ip_address=ip).exists()
        if not query:
            obj = Ip.objects.create(ip_address=ip, last_excessive_request_time=datetime.now())
            obj.save()
        else:
            obj = Ip.objects.get(ip_address=ip)

        self.check_excessive_requests(request, obj)
        
    def check_excessive_requests(self, request, obj):
        if not request.user.is_superuser:
            minus = datetime.now().timestamp() - obj.last_excessive_request_time.timestamp()
            block_time_minute = 10
            minimum_difference_float = 1.0
            max_count = 5
        
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
                    username = request.user.username
                    email = request.user.email
                    user = User.objects.get(username=username, email=email)
                    user.excessive_requests_count += 1
                    user.save()
            else:
                difference_block_time = obj.last_excessive_request_time + timedelta(minutes=block_time_minute)

                if datetime.now().timestamp() < difference_block_time.timestamp():
                    diffrence = difference_block_time.timestamp() - datetime.now().timestamp()
                    raise Http404(f"You have been blocked for {round(diffrence, 2)} seconds due to excessive requests!")
                else:
                    obj.excessive_requests_count = 0
                    obj.save()
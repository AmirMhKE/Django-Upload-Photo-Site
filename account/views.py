from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from .mixins import LoginRequiredMixin

User = get_user_model()

class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "account/statistics.html"

    def get_context_data(self, **kwargs):
        this_user = User.objects.get(username=self.request.user.username, email=self.request.user.email)
        context = super().get_context_data(**kwargs)
        context.update({
            "post_count": this_user.posts.count(),
            "like_count": this_user.likes.count(),
            "all_requests_count": this_user.all_requests_count,
            "requests_search_count": this_user.requests_search_count,
            "requests_download_count": this_user.requests_download_count,
            "excessive_requests_count": this_user.excessive_requests_count,
        })
        return context
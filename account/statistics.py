from datetime import datetime, timedelta

from app.models import Download, Hit, Like
from django.db.models import Count, F
from jdatetime import date


def user_posts_statistics(user, days_ago, reverse=None):
    """
    This function returns statistics of user posts 
    (number of hits, likes, downloads per day) 
    to the number of 'days_ago' for the user.
    If the 'reverse' parameter is true, 
    it returns the statistics in reverse.
    """
    if reverse is None:
        reverse = False

    start_time = datetime.now() - timedelta(days=days_ago)

    hit_query = Hit.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time).values(created_date=F("created__date")) \
    .annotate(number=Count("pk")).order_by("-created_date")

    like_query = Like.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time, status=True).values(created_date=F("updated__date")) \
    .annotate(number=Count("pk")).order_by("-created_date")

    download_query = Download.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time).values(created_date=F("created__date")) \
    .annotate(number=Count("pk")).order_by("-created_date")

    created_dates = hit_query.values("created_date").union(
        like_query.values("created_date"), 
        download_query.values("created_date")
    ).values_list("created_date").order_by("-created_date")

    hits = list(map(lambda date: hit_query.get(created_date=date[0])["number"]
    if hit_query.filter(created_date=date[0]).exists() else 0, created_dates.iterator()))

    likes = list(map(lambda date: like_query.get(created_date=date[0])["number"]
    if like_query.filter(created_date=date[0]).exists() else 0, created_dates.iterator()))

    downloads = list(map(lambda date: download_query.get(created_date=date[0])["number"]
    if download_query.filter(created_date=date[0]).exists() else 0, created_dates.iterator()))

    dates = list(map(lambda date_: date.fromgregorian(date=date_[0])
    .strftime("%Y/%m/%d"), created_dates.iterator()))

    if reverse:
        hits, likes, downloads, dates = hits[::-1], likes[::-1], downloads[::-1], dates[::-1]

    return {
        "dates": dates,
        "hits": hits,
        "likes": likes,
        "downloads": downloads
    }

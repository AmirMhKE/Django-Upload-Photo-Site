from datetime import datetime, timedelta

import jdatetime
from app.models import Download, Hit, Like
from django.db.models import F, Count


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

    created_dates = tuple((
        date[0] for date in

        Hit.objects.filter(post__publisher__id=user.id, created__date__gte=start_time)
        .values(created_date=F("created__date")).union(

            Like.objects.filter(post__publisher__id=user.id, 
            created__date__gte=start_time, status=True)
            .values(created_date=F("updated__date")),

            Download.objects.filter(post__publisher__id=user.id, 
            created__date__gte=start_time)
            .values(created_date=F("created__date"))

        ).values_list("created_date").iterator()
    ))

    hit_query = Hit.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time).values(created_date=F("created__date")) \
    .annotate(number=Count("pk")).order_by("created_date")

    like_query = Like.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time, status=True).values(created_date=F("updated__date")) \
    .annotate(number=Count("pk")).order_by("created_date")

    download_query = Download.objects.filter(post__publisher__id=user.id, 
    created__date__gte=start_time).values(created_date=F("created__date")) \
    .annotate(number=Count("pk")).order_by("created_date")

    hits = [*(
        hit_query.filter(created_date=date)[0]["number"] 
        if hit_query.filter(created_date=date).exists() 
        else 0 for date in created_dates
    )]

    likes = [*(
        like_query.filter(created_date=date)[0]["number"] 
        if like_query.filter(created_date=date).exists() 
        else 0 for date in created_dates
    )]

    downloads = [*(
        download_query.filter(created_date=date)[0]["number"] 
        if download_query.filter(created_date=date).exists() 
        else 0 for date in created_dates
    )]

    dates = [jdatetime.date.fromgregorian(date=date)
    .strftime("%Y/%m/%d") for date in created_dates]

    if reverse:
        hits, likes, downloads, dates = hits[::-1], likes[::-1], downloads[::-1], dates[::-1]

    return {
        "dates": dates,
        "hits": hits,
        "likes": likes,
        "downloads": downloads
    }

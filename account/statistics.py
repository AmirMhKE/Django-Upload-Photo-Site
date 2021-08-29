import jdatetime
from datetime import datetime, timedelta

from app.models import Hit, Like, Download

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

    query1 = Hit.objects.filter(post__publisher__id=user.id)
    query2 = Like.objects.active().filter(post__publisher__id=user.id)
    query3 = Download.objects.filter(post__publisher__id=user.id)

    hits, likes, downloads = [], [], []
    for day in range(days_ago + 1):
        get_date = datetime.now() - timedelta(days=day)
        get_jdate = jdatetime.date.fromgregorian(date=get_date)

        hit_query = query1.filter(created__date=get_date)
        like_query = query2.filter(created__date=get_date)
        download_query = query3.filter(created__date=get_date)

        if hit_query.exists() or like_query.exists() or download_query.exists():
            hits.append((get_jdate.strftime("%Y/%m/%d"), hit_query.count()))
            likes.append((get_jdate.strftime("%Y/%m/%d"), like_query.count()))
            downloads.append((get_jdate.strftime("%Y/%m/%d"), download_query.count()))

    if reverse:
        hits, likes, downloads = hits[::-1], likes[::-1], downloads[::-1]

    return {
        "hits": hits,
        "likes": likes,
        "downloads": downloads
    }

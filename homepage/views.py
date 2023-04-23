import random as r

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import cache_control

from homepage.middleware import ForwardParametersMiddleware
from reader.middleware import OnlineNowMiddleware
from reader.models import Chapter
from utils.middleware import NotifactionMiddleWare


@staff_member_required
@cache_control(public=True, max_age=30, s_maxage=30)
def admin_home(request):
    online = cache.get("online_now")
    peak_traffic = cache.get("peak_traffic")
    return render(
        request,
        "homepage/admin_home.html",
        {
            "online": len(online) if online else 0,
            "peak_traffic": peak_traffic,
            "template": "home",
            "version_query": settings.STATIC_VERSION,
        },
    )


@decorator_from_middleware(OnlineNowMiddleware)
@decorator_from_middleware(NotifactionMiddleWare)
def home(request):
    return render(
        request,
        "homepage/homepage.html",
        {
            "abs_url": request.build_absolute_uri(),
            "api_path": "/api",
            "relative_url": "",
            "canonical_url": settings.CANONICAL_ROOT_DOMAIN + "/",
            "page_title": "Chào mừng đến lớp học đề cao thực lực",
            "template": "home",
            "version_query": settings.STATIC_VERSION,
            "media_url": settings.MEDIA_URL,
        },
    )


@cache_control(public=True, max_age=3600, s_maxage=300)
@decorator_from_middleware(OnlineNowMiddleware)
@decorator_from_middleware(NotifactionMiddleWare)
def about(request):
    return render(
        request,
        "homepage/about.html",
        {
            "relative_url": "about/",
            "template": "about",
            "page_title": "About",
            "version_query": settings.STATIC_VERSION,
        },
    )


@decorator_from_middleware(ForwardParametersMiddleware)
def main_series_chapter(request, chapter):
    return redirect(
        "reader-manga-chapter", "manga-nam-hai", chapter, "1"
    )


@decorator_from_middleware(ForwardParametersMiddleware)
def main_series_page(request, chapter, page):
    return redirect(
        "reader-manga-chapter", "manga-nam-hai", chapter, page
    )


@decorator_from_middleware(ForwardParametersMiddleware)
def latest(request):
    latest_chap = cache.get("latest_chap")
    if not latest_chap:
        latest_chap = (
            Chapter.objects.order_by("-chapter_number")
            .filter(series__slug="manga-nam-hai")[0]
            .slug_chapter_number()
        )
        cache.set("latest_chap", latest_chap, 3600 * 96)
    return redirect(
        "reader-manga-chapter", "manga-nam-hai", latest_chap, "1"
    )


@decorator_from_middleware(ForwardParametersMiddleware)
def random(request):
    random_opts = cache.get("random_opts")
    if not random_opts:
        random_opts = [
            ch.slug_chapter_number()
            for ch in (
                Chapter.objects.order_by("-chapter_number").filter(
                    series__slug="manga-nam-nhat"
                )
            )
        ]
        cache.set("random_opts", random_opts, 3600 * 96)
    return redirect(
        "reader-manga-chapter",
        "manga-nam-nhat",
        r.choice(random_opts),
        "1",
    )


def handle404(request, exception):
    return render(request, "homepage/404_page.html", status=404)


def handle500(request):
    return render(request, "homepage/500_page.html", status=500)

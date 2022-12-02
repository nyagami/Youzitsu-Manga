from django.urls import re_path
from reader import views

urlpatterns = [
    re_path(
        r"^manga/(?P<series_slug>[\w-]+)/$", views.series_info, name="reader-manga"
    ),
    re_path(
        r"^series/(?P<series_slug>[\w-]+)/$", views.series_info, name="reader-series"
    ),
    re_path(
        r"^manga/(?P<series_slug>[\w-]+)/admin$",
        views.series_info_admin,
        name="reader-manga-admin",
    ),
    re_path(
        r"^series/(?P<series_slug>[\w-]+)/admin$",
        views.series_info_admin,
        name="reader-series-admin",
    ),
    re_path(
        r"^manga/(?P<series_slug>[\w-]+)/(?P<chapter>[\d-]{1,9})/$",
        views.reader,
        name="reader-manga-chapter-shortcut",
    ),
    re_path(
        r"^series/(?P<series_slug>[\w-]+)/(?P<chapter>[\d-]{1,9})/$",
        views.reader,
        name="reader-series-chapter-shortcut",
    ),
    re_path(
        r"^manga/(?P<series_slug>[\w-]+)/(?P<chapter>[\d-]{1,9})/(?P<page>[\d]{1,9})/$",
        views.reader,
        name="reader-manga-chapter",
    ),
    re_path(
        r"^series/(?P<series_slug>[\w-]+)/(?P<chapter>[\d-]{1,9})/(?P<page>[\d]{1,9})/$",
        views.reader,
        name="reader-series-chapter",
    ),
    re_path(
        r"^manga/(?P<url_str>[\w-]+)/(?P<series_slug>[\w-]+)/$",
        views.series_info_canonical,
        name="reader-manga-canonical",
    ),
    re_path(r"^update_view_count/", views.hit_count, name="reader-view-count"),
]

from django.urls import re_path, path

from api import views

urlpatterns = [
    re_path(
        r"^series/(?P<series_slug>[\w-]+)/$",
        views.get_series_data,
        name="api-series_data",
    ),
    re_path(
        r"^series_page_data/(?P<series_slug>[\w-]+)/$",
        views.get_series_page_data_req,
        name="api-series-page-data",
    ),
    re_path(r"^get_all_series/", views.get_all_series, name="api-get-all-series"),
    re_path(
        r"^get_groups/(?P<series_slug>[\w-]+)/", views.get_groups, name="api-groups"
    ),
    re_path(r"^get_all_groups/", views.get_all_groups, name="api-all-groups"),
    re_path(
        r"^download_chapter/(?P<series_slug>[\w-]+)/(?P<chapter>[\d-]{1,9})/$",
        views.download_chapter,
        name="api-chapter-download",
    ),
    re_path(
        r"^upload_new_chapter/(?P<series_slug>[\w-]+)/",
        views.upload_new_chapter,
        name="api-chapter-upload",
    ),
    re_path(
        r"^get_volumes_by_series_slug/(?P<series_slug>[\w-]+)/$",
        views.get_volumes_by_series_slug,
        name="api-get-volumes-by-series-slug",
    ),
    re_path(
        r"^get_volume_covers/(?P<series_slug>[\w-]+)/",
        views.get_volume_covers,
        name="api-get-volume-covers",
    ),
    re_path(
        r"^get_volume_cover/(?P<series_slug>[\w-]+)/(?P<volume_number>[\d-]{1,9})/$",
        views.get_volume_cover,
        name="api-get-volume-cover",
    ),
    re_path(
        r"^search_index/(?P<series_slug>[\w-]+)/",
        views.search_index,
        name="api-search-index",
    ),

    # user info
    path("get_user_info/", views.get_user_info, name="api-get-user-info"),
]

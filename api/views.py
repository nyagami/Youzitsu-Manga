import json
import os
import time
import zipfile
from datetime import datetime
from hashlib import sha512

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from reader.models import Chapter, ChapterIndex, Group, Series, Volume
from reader.views import series_page_data

from user.models import Profile
from utils.models import Comment, Notification
from utils.consumers import NotifcationConsumer, CommentConsumer
from colorfield.fields import color_hex_validator


from .api import (
    all_groups,
    chapter_post_process,
    clear_pages_cache,
    clear_series_cache,
    create_chapter_obj,
    get_chapter_preferred_sort,
    series_data_cache,
    zip_chapter,
)


@cache_control(public=True, max_age=30, s_maxage=30)
def get_series_data(request, series_slug):
    series_api_data = cache.get(f"series_api_data_{series_slug}")
    if not series_api_data:
        series_api_data = series_data_cache(series_slug)
    return HttpResponse(json.dumps(series_api_data), content_type="application/json")


@cache_control(public=True, max_age=60, s_maxage=60)
def get_series_page_data_req(request, series_slug):
    data = series_page_data(request, series_slug)
    data["version_query"] = settings.STATIC_VERSION
    return HttpResponse(json.dumps(data), content_type="application/json")


@cache_control(public=True, max_age=900, s_maxage=900)
def get_all_series(request):
    all_series_data = cache.get('all-series-data')
    if not all_series_data:
        all_series = Series.objects.all().select_related("author", "artist")
        all_series_data = {}
        for series in all_series:
            vols = Volume.objects.filter(series=series).order_by("-volume_number")
            cover_url = f"/media/{series.embed_image}"
            if series.use_latest_vol_cover_for_embed:
                for vol in vols:
                    if vol.volume_cover:
                        cover_url = f"/media/{vol.volume_cover}"
                        break
            chapters = Chapter.objects.filter(series=series)
            last_updated = None
            for ch in chapters:
                if not last_updated or ch.uploaded_on > last_updated:
                    last_updated = ch.uploaded_on
            all_series_data[series.name] = {
                "author": series.author.name,
                "artist": series.artist.name,
                "description": series.synopsis,
                "slug": series.slug,
                "cover": cover_url,
                "groups": all_groups(),
                "last_updated": int(datetime.timestamp(last_updated))
                if last_updated
                else 0,
                "volumes": [{"num": vol.volume_number, "color": vol.color_theme} for vol in vols],
            }
        cache.set("all_series_data", all_series_data, 3600 * 12)
    return HttpResponse(json.dumps(all_series_data), content_type="application/json")


@cache_control(public=True, max_age=7200, s_maxage=7200)
def get_groups(request, series_slug):
    groups_data = cache.get(f"groups_data_{series_slug}")
    if not groups_data:
        groups_data = {
            str(ch.group.id): ch.group.name
            for ch in Chapter.objects.filter(series__slug=series_slug).select_related(
                "group"
            )
        }
        cache.set(f"groups_data_{series_slug}", groups_data, 3600 * 12)
    return HttpResponse(
        json.dumps({"groups": groups_data}), content_type="application/json"
    )


@cache_control(public=True, max_age=7200, s_maxage=7200)
def get_all_groups(request):
    return HttpResponse(json.dumps(all_groups()), content_type="application/json")


# @cache_control(public=True, max_age=43200, s_maxage=43200)
# def download_volume(request, series_slug, volume):
#     zip_filename = f"{series_slug}_vol_{volume}.zip"
#     zip_path = os.path.join(settings.MEDIA_ROOT, "manga", series_slug, zip_filename)
#     if os.path.exists(zip_path) and not (
#         time.time() - os.stat(zip_path).st_mtime > (3600 * 8)
#     ):
#         with open(
#             os.path.join(settings.MEDIA_ROOT, "manga", series_slug, zip_filename), "rb"
#         ) as fh:
#             zip_file = fh.read()
#     else:
#         zip_file, zip_filename = zip_volume(series_slug, volume)
#     resp = HttpResponse(zip_file, content_type="application/x-zip-compressed")
#     resp["Content-Disposition"] = "attachment; filename=%s" % zip_filename
#     return resp


@cache_control(public=True, max_age=21600, s_maxage=21600)
def download_chapter(request, series_slug, chapter):
    group = request.GET.get("group", None)
    chapter_number = float(chapter.replace("-", "."))
    if not group:
        ch_obj = None
        ch_qs = Chapter.objects.filter(
            series__slug=series_slug, chapter_number=chapter_number
        )
        if not ch_qs:
            return HttpResponseBadRequest()
        preferred_sort = get_chapter_preferred_sort(ch_qs.first())
        if preferred_sort:
            for group in preferred_sort:
                ch_obj = ch_qs.filter(group__id=int(group)).first()
                if ch_obj:
                    break
        if not ch_obj:
            ch_obj = ch_qs.first()
    else:
        if not group.isdigit():
            return HttpResponseBadRequest()
        ch_obj = Chapter.objects.get(
            series__slug=series_slug,
            chapter_number=chapter_number,
            group__id=int(group),
        )
    group = str(ch_obj.group.id)
    chapter_dir = os.path.join(
        settings.MEDIA_ROOT, "manga", series_slug, "chapters", ch_obj.folder
    )
    zip_chapter_file = f"{group}_{ch_obj.slug_chapter_number()}.zip"
    zip_path = os.path.join(chapter_dir, zip_chapter_file)
    if os.path.exists(zip_path) and not (
        time.time() - os.stat(zip_path).st_mtime > (3600 * 8)
    ):
        with open(os.path.join(chapter_dir, zip_chapter_file), "rb") as f:
            zip_file = f.read()
    else:
        zip_file, _, _ = zip_chapter(ch_obj)
    resp = HttpResponse(zip_file, content_type="application/x-zip-compressed")
    resp[
        "Content-Disposition"
    ] = f"attachment; filename={ch_obj.slug_chapter_number()}.zip"
    return resp


def upload_new_chapter(request, series_slug):
    if request.method == "POST" and request.user and request.user.is_staff:
        group = Group.objects.get(name=request.POST["scanGroup"])
        series = Series.objects.get(slug=series_slug)
        chapter_number = float(request.POST["chapterNumber"])
        volume = request.POST["volumeNumber"]
        title = request.POST["chapterTitle"]
        ch_obj, chapter_folder, group_folder, is_update = create_chapter_obj(
            chapter_number, group, series, volume, title
        )
        with zipfile.ZipFile(request.FILES["chapterPages"]) as zip_file:
            zipped_pages = zip_file.namelist()
            try:
                from decimal import Decimal
                all_pages = sorted(zipped_pages, key=lambda x: Decimal(x.split('/')[-1].rsplit('.', 1)[0]))
            except Exception:
                all_pages = sorted(zipped_pages)
            padding = len(str(len(all_pages)))
            for idx, page in enumerate(all_pages):
                extension = page.rsplit(".", 1)[-1]
                page_file = f"{str(idx+1).zfill(padding)}.{extension}"
                with open(
                    os.path.join(chapter_folder, group_folder, page_file), "wb"
                ) as f:
                    f.write(zip_file.read(page))
        chapter_post_process(ch_obj, is_update=is_update)
        return HttpResponse(
            json.dumps({"response": "success"}), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"response": "failure"}), content_type="application/json"
        )


def get_volumes_by_series_slug(request, series_slug):
    series = Series.objects.filter(slug=series_slug).first()
    volumes = Volume.objects.filter(series=series)
    volumes_list = [
        {
            "number": volume.volume_number,
            "color": volume.color_theme,
        } for volume in volumes
    ]
    return HttpResponse(json.dumps({"volumes_list": volumes_list}), content_type="application/json", status="200")


@csrf_exempt
@cache_control(public=True, max_age=3600, s_maxage=3600)
def get_volume_covers(request, series_slug):
    covers = cache.get(f"vol_covers_{series_slug}")
    if not covers:
        series = Series.objects.filter(slug=series_slug).first()
        if series:
            volume_covers = (
                Volume.objects.filter(series=series)
                .order_by("volume_number")
                .values_list("volume_number", "volume_cover")
            )
            covers = [
                [
                    cover[0],
                    f"/media/{str(cover[1])}",
                    f"/media/{str(cover[1]).rsplit('.', 1)[0]}.webp",
                    f"/media/{str(cover[1]).rsplit('.', 1)[0]}_blur.{str(cover[1]).rsplit('.', 1)[1]}",
                ]
                for cover in volume_covers
                if cover[1]
            ]
            cache.set(f"vol_covers_{series_slug}", covers)
            return HttpResponse(json.dumps({"covers": covers}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"covers": covers}), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json", status="204")


@cache_control(public=True, max_age=3600, s_maxage=3600)
def get_volume_cover(request, series_slug, volume_number):
    cover = cache.get(f"vol_cover{volume_number}_{series_slug}")
    if not cover:
        series = Series.objects.filter(slug=series_slug).first()
        if series:
            volume = Volume.objects.filter(
                series=series, volume_number=volume_number
            ).first()
            if volume:
                cover = [
                    volume.volume_number,
                    f"/media/{str(volume.volume_cover)}",
                    f"/media/{str(volume.volume_cover).rsplit('.', 1)[0]}.webp",
                    f"""/media/{str(volume.volume_cover).rsplit('.', 1)[0]}_blur.{
                        str(volume.volume_cover).rsplit('.', 1)[1]}""",
                ]
                cache.set(f"vol_cover{volume_number}_{series_slug}", cover)
                return HttpResponse(json.dumps(cover), content_type="application/json")
    else:
        return HttpResponse(json.dumps(cover), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json", status="204")


@csrf_exempt
def search_index(request, series_slug):
    if request.method == "POST":
        series = Series.objects.get(slug=series_slug)
        search_query = request.POST["searchQuery"]
        search_results = {}
        for word in set(search_query.split()[:20]):
            word_query = ChapterIndex.objects.filter(
                word__startswith=word.upper(), series=series
            )
            search_results[word] = {}
            for word_obj in word_query:
                chapter_and_pages = json.loads(word_obj.chapter_and_pages)
                search_results[word][word_obj.word] = chapter_and_pages
        return HttpResponse(json.dumps(search_results), content_type="application/json")
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")


@csrf_exempt
def clear_cache(request):
    if request.method == "POST" and request.user and request.user.is_staff:
        if request.POST["clear_type"] == "all":
            clear_pages_cache()
            response = "Cleared all cache"
        elif request.POST["clear_type"] == "chapter":
            for series_slug in Series.objects.all().values_list("slug"):
                clear_series_cache(series_slug)
            response = "Cleared series cache"
        else:
            response = "Not a valid option"
        return HttpResponse(
            json.dumps({"response": response}), content_type="application/json"
        )
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")


def series_data_slug(request):
    if request.method == "GET":
        series = [series.slug for series in Series.objects.all().order_by("id")]
        return HttpResponse(json.dumps(series), content_type="application/json")


@csrf_exempt
def update_theme(request):
    if request.user.is_authenticated is False or request.method != 'POST':
        return HttpResponseBadRequest()

    profile = Profile.objects.get(user=request.user)
    theme = request.POST.get('theme')
    primary_color = request.POST.get('primary_color')
    text_color = request.POST.get('text_color')
    accent_color = request.POST.get('accent_color')
    reader_background = request.POST.get('reader_background')
    try:
        Profile.valid_theme(theme)
        color_hex_validator(primary_color)
        color_hex_validator(text_color)
        color_hex_validator(accent_color)
        color_hex_validator(reader_background)
    except Exception:
        return HttpResponseBadRequest()

    profile.theme = theme
    profile.primary_color = primary_color
    profile.text_color = text_color
    profile.accent_color = accent_color
    profile.reader_background = reader_background
    profile.save()
    return HttpResponse(json.dumps({"response": "success"}), content_type="application/json", status=200)


def post_comment(request):
    if request.user.is_authenticated is False or request.method != 'POST':
        return HttpResponseBadRequest()

    article = request.POST.get('article')
    if not article or len(article) < 3 or article[1] != '_':
        return HttpResponseBadRequest()

    parent = request.POST.get('parent')
    if parent:
        if len(parent) > 10:
            return HttpResponseBadRequest()
        try:
            parent = int(parent)
        except ValueError:
            return HttpResponseBadRequest()
        if parent == -1:
            parent = None
        else:
            try:
                parent = Comment.objects.get(visible=True, id=parent, article=article)
            except ValueError:
                return HttpResponseBadRequest()

    if not parent:
        deepth = 0
    else:
        deepth = parent.deepth + 1
        if deepth > 2:
            deepth = 2
            parent = parent.parent
    content = request.POST.get('content')
    if not content:
        return HttpResponseBadRequest()
    media = request.FILES.get('media')
    media_url = ''
    if media:
        media = media.read()
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'comment'), exist_ok=True)
        hash = sha512(media).hexdigest() + '.jpeg'
        media_url = os.path.join(settings.MEDIA_ROOT, 'comment', hash)
        if not os.path.exists(media_url):
            with open(media_url, 'wb') as f:
                f.write(media)
        media_url = '/media/comment/' + hash
    comment_obj = Comment.objects.create(author=request.user.profile, article=article, parent=parent,
                                         deepth=deepth, content=content, media_url=media_url)

    # socketing
    comment = model_to_dict(comment_obj)
    comment['author'] = model_to_dict(request.user.profile)
    comment['username'] = request.user.username
    comment['created_on'] = f'{comment_obj.created_on.date()} {comment_obj.created_on.time()}'
    CommentConsumer.send_comment(article, comment)

    # who is replied
    reply = None
    if parent:
        reply = parent.author.user.username

    if reply:
        try:
            receiver = User.objects.get(username=reply)
            Notification.objects.create(sender=request.user.profile, receiver=receiver.profile,
                                        title='Đã hồi bình luận', href='#', content=content, unread=1)
            NotifcationConsumer.notify_one(comment, reply)
        except ValueError:
            pass

    # people who are tagged in
    # mentions = request.POST.get('mentions')
    # if mentions:
    #     mentions = mentions.trim().split()
    #     NotifcationConsumer.notify_all(comment, mentions)

    return HttpResponse(json.dumps({"response": "success"}), content_type='application/json', status=200)


def delete_comment(request):
    if request.user.is_authenticated is False or request.method != 'POST':
        return HttpResponseBadRequest()
    id = request.POST.get('id')
    try:
        comment = Comment.objects.get(id=id)
        if comment.author.user.username != request.user.username:
            raise ValueError
        comment.delete()
    except ValueError:
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps({"response": "success"}), content_type='application/json', status=200)


def update_comment(request):
    if request.user.is_authenticated is False or request.method != 'POST':
        return HttpResponseBadRequest()
    id = request.POST.get('id')
    try:
        comment = Comment.objects.get(id=id)
        if comment.author.user.username != request.user.username:
            raise ValueError
        content = request.POST.get('content')
        mention = request.POST.get('mention')
        if not content:
            raise ValueError
        comment.update(content=content, mention=mention)
    except ValueError:
        return HttpResponseBadRequest()

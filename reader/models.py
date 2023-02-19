import os
from datetime import datetime, timezone
from random import randint
from colorfield.fields import ColorField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


MANGADEX = "MD"
SCRAPING_SOURCES = ((MANGADEX, "MangaDex"),)


class HitCount(models.Model):
    content = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    hits = models.PositiveIntegerField(("Hits"), default=0)


class Person(models.Model):
    name = models.CharField(max_length=200)
    japan_name = models.CharField(max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Nhóm dịch/scan'


def embed_image_path(instance, filename):
    return os.path.join("manga", instance.slug, "static", str(filename))


def new_volume_folder(instance):
    return os.path.join(
        "manga", instance.series.slug, "volume_covers", str(instance.volume_number),
    )


def new_volume_path_file_name(instance, filename):
    _, ext = os.path.splitext(filename)
    new_filename = str(randint(10000, 99999)) + ext
    return os.path.join(new_volume_folder(instance), new_filename,)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    index = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Thể loại"
        ordering = ("index",)


class Series(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='category')
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="series_author",
    )
    artist = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="series_artist",
    )
    synopsis = models.TextField(blank=True, null=True, verbose_name='Tóm tắt')
    alternative_titles = models.TextField(blank=True, null=True)
    next_release_page = models.BooleanField(default=False)
    next_release_time = models.DateTimeField(
        default=None, blank=True, null=True, db_index=True
    )
    next_release_html = models.TextField(blank=True, null=True)
    indexed = models.BooleanField(default=False)
    preferred_sort = models.CharField(max_length=200, blank=True, null=True)
    scraping_enabled = models.BooleanField(default=False)
    scraping_source = models.CharField(
        max_length=2, choices=SCRAPING_SOURCES, default=MANGADEX
    )
    scraping_identifiers = models.TextField(blank=True, null=True)
    use_latest_vol_cover_for_embed = models.BooleanField(default=False)
    embed_image = models.ImageField(upload_to=embed_image_path, blank=True, null=True)
    canonical_series_url_filler = models.CharField(
        max_length=24,
        blank=True,
        null=True,
        help_text="""Adds this text to the canonical url of the series' series page.
                     Useful to avoid blacklists of... many varieties.""",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.canonical_series_url_filler:
            return f"/read/series/{self.canonical_series_url_filler}/{self.slug}/"
        else:
            return f"/read/series/{self.slug}/"

    def get_latest_volume_cover_path(self):
        vols = Volume.objects.filter(series=self).order_by("-volume_number")
        for vol in vols:
            if vol.volume_cover:
                cover_vol_url = f"/media/{vol.volume_cover}"
                return cover_vol_url, cover_vol_url.rsplit(".", 1)[0] + ".webp"
        else:
            return "", ""

    def get_embed_image_path(self):
        if self.use_latest_vol_cover_for_embed:
            embed_image, _ = self.get_latest_volume_cover_path()
            return embed_image
        elif self.embed_image:
            return f"/media/{self.embed_image}"
        else:
            return ""

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Tác phẩm"


class Volume(models.Model):
    volume_number = models.FloatField(blank=False, null=False, db_index=True)
    series = models.ForeignKey(
        Series, blank=False, null=False, on_delete=models.CASCADE, related_name="series",
    )
    color_theme = ColorField(default='#FF0000')
    volume_cover = models.ImageField(blank=True, upload_to=new_volume_path_file_name)

    def clean_volume_number(self):
        return (
            str(int(self.volume_number))
            if self.volume_number % 1 == 0
            else str(self.volume_number)
        )

    class Meta:
        unique_together = (
            "volume_number",
            "series",
        )


class Chapter(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    chapter_number = models.FloatField(blank=False, null=False, db_index=True)
    folder = models.CharField(max_length=255, blank=True, null=True)
    volume = models.PositiveSmallIntegerField(
        blank=True, null=True, default=None, db_index=True
    )
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    uploaded_on = models.DateTimeField(
        default=None, blank=True, null=True, db_index=True
    )
    updated_on = models.DateTimeField(
        default=None, blank=True, null=True, db_index=True
    )
    version = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    preferred_sort = models.CharField(max_length=200, blank=True, null=True)
    scraper_hash = models.CharField(max_length=32, blank=True)
    reprocess_metadata = models.BooleanField(
        default=False,
        help_text="""Check this and save to recreate/reprocess other chapter data
                     (preview versions of the chapter and chapter index). This field will automatically uncheck on save.
                     Chapter reindexing will be kicked off in the background.""",
    )

    def clean_chapter_number(self):
        return (
            str(int(self.chapter_number))
            if self.chapter_number % 1 == 0
            else str(self.chapter_number)
        )

    def slug_chapter_number(self):
        return self.clean_chapter_number().replace(".", "-")

    def get_chapter_time(self):
        upload_date = self.uploaded_on
        upload_time = (
            datetime.utcnow().replace(tzinfo=timezone.utc) - upload_date
        ).total_seconds()
        days = int(upload_time // (24 * 3600))
        upload_time = upload_time % (24 * 3600)
        hours = int(upload_time // 3600)
        upload_time %= 3600
        minutes = int(upload_time // 60)
        upload_time %= 60
        seconds = int(upload_time)
        if days == 0 and hours == 0 and minutes == 0:
            upload_date = f"{seconds} giây trước"
        elif days == 0 and hours == 0:
            upload_date = f"{minutes} phút trước"
        elif days == 0:
            upload_date = f"{hours} giờ trước"
        elif days < 7:
            upload_date = f"{days} ngày trước"
        else:
            upload_date = upload_date.strftime("%d-%m-%Y")
        return upload_date

    def __str__(self):
        return f"{self.chapter_number} - {self.title}"

    def get_absolute_url(self):
        return f"/read/series/{self.series.slug}/{Chapter.slug_chapter_number(self)}/1"

    class Meta:
        ordering = ("chapter_number",)
        unique_together = (
            "chapter_number",
            "series",
            "group",
        )


class ChapterIndex(models.Model):
    word = models.CharField(max_length=128, db_index=True)
    chapter_and_pages = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return self.word

    class Meta:
        unique_together = (
            "word",
            "series",
        )


def path_file_name(instance, filename):
    return os.path.join(
        "manga",
        instance.series.slug,
        "volume_covers",
        str(instance.volume_number),
        filename,
    )

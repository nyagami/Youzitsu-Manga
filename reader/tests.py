from django.test import TestCase
from django.conf import settings

import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFilter

from .models import (
    Creator, Group, Series, Volume, Chapter
)

WIDTH = 850
HEIGHT = 1250
PAGES = 18
PROCESSES = 15


def create_img(path):
    if not os.path.isfile(path):
        width = WIDTH
        height = HEIGHT
        if "shrunk" in path:
            width = 85
            height = 125
        img = Image.new(
            "RGB",
            (width, height),
            color=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ),
        )
        ImageDraw.Draw(img).text(
            (width // 10, height // 10), os.path.basename(path), fill=(0, 0, 0)
        )
        if "blur" in path:
            img = img.filter(ImageFilter.GaussianBlur(radius=10))
        img.save(path)
        return True


class ReaderTest(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        super().setUpTestData()
        self.author = Creator.objects.create(name="author")
        self.artist = Creator.objects.create(name="artist")
        self.group = Group.objects.create(name="group")
        self.series = Series.objects.create(
            name="series", slug="series", author=self.author, artist=self.artist,
            synopsis="synopsis", alternative_titles="alternative_titles",
        )
        self.volume = Volume.objects.create(volume_number=1, series=self.series)
        self.chapter = Chapter.objects.create(
            series=self.series, title="chapter", chapter_number=1, volume=1,
            group=self.group, folder="chapter_folder"
        )
        self.generate_images(self)
        self.series.embed_image = os.path.join(self.series_dir, 'embed_img.jpg')
        self.series.save()
        self.volume.volume_cover = os.path.join(self.volume_dir, 'cover.jpg')
        self.volume.save()

    def generate_images(self):
        self.series_dir = os.path.join(settings.MEDIA_ROOT, 'manga', self.series.slug, 'static')
        self.volume_dir = os.path.join(settings.MEDIA_ROOT, 'manga', self.series.slug,
                                       'volume_covers', self.volume.clean_volume_number())
        self.chapter_dir = os.path.join(settings.MEDIA_ROOT, 'manga', self.series.slug, 'chapters',
                                        self.chapter.folder)
        os.makedirs(self.series_dir, exist_ok=True)
        os.makedirs(self.volume_dir, exist_ok=True)
        os.makedirs(os.path.join(self.chapter_dir, str(self.chapter.group.id)), exist_ok=True)
        os.makedirs(os.path.join(self.chapter_dir, f'{str(self.chapter.group.id)}_shrunk'), exist_ok=True)
        os.makedirs(os.path.join(self.chapter_dir, f'{str(self.chapter.group.id)}_shrunk_blur'), exist_ok=True)
        img_paths = []
        img_paths.append(os.path.join(self.series_dir, 'embed_img.jpg'))
        img_paths.append(os.path.join(self.volume_dir, 'cover.jpg'))
        for page_num in range(1, PAGES + 1):
            img_paths.append(
                os.path.join(self.chapter_dir, str(self.chapter.group.id), f'{page_num:03}.jpg')
            )
            img_paths.append(
                os.path.join(self.chapter_dir, f'{str(self.chapter.group.id)}_shrunk', f'{page_num:03}.jpg')
            )
            img_paths.append(
                os.path.join(self.chapter_dir, f'{str(self.chapter.group.id)}_shrunk_blur', f'{page_num:03}.jpg')
            )

        for path in img_paths:
            create_img(path)

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'manga', self.series.slug))

    def test_api_series(self):
        self.assertTrue(True)

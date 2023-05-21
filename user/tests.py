from django.test import TestCase
from utils.tests import Common


class ProfileTest(Common, TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        super().setUpTestData()
        self.profile = self.profiles['normal']

    def setUp(self):
        self.profile.refresh_from_db()

    def test_default_display_name(self):
        self.assertEqual(self.profile.display_name, self.users['normal'].username)

    def test_default_theme(self):
        self.assertEqual(self.profile.theme, 'Dark')

    def test_default_avatar(self):
        self.assertEqual(self.profile.avatar, '/static/img/unknown_user.jpeg')

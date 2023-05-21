from django.contrib.auth.models import AnonymousUser, User
from user.models import Profile


class Common:
    @classmethod
    def setUpTestData(self):
        self.users = {
            'normal': User.objects.create(username='normal'),
            'superuser': User.objects.create(username='admin', is_superuser=True, is_staff=True),
            'anonymous': AnonymousUser(),
        }

        self.profiles = {
            'normal': Profile.objects.get(user=self.users['normal']),
            'superuser': Profile.objects.get(user=self.users['superuser']),
        }

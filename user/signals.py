from user.models import Profile
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user = instance)
        profile.display_name = instance.username
        profile.save()

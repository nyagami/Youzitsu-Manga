from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", )

    readonly_fields = ["avatar"]


admin.site.register(Profile, ProfileAdmin)

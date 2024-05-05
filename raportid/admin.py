from django.contrib import admin

from raportid.models import EnterpriseGroups
from raportid.models import Enterprises


@admin.register(EnterpriseGroups)
class EnterpriseGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'assets_value', 'enterprise']
    search_fields = ['name', 'enterprise__name']
    autocomplete_fields = ['enterprise']


@admin.register(Enterprises)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'assets_value', 'group', 'owner', 'share_percentage']
    search_fields = ['name', 'group__name', 'owner__name']
    autocomplete_fields = ['group', 'owner']

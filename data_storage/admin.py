from django.contrib import admin

from data_storage.models import Party, EnterpriseGroup, PhysicalPerson, LegalPerson, Assets, Ownership


# Register your models here.
@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'party_type', 'name']
    search_fields = ['party_type', 'name']
    list_filter = ['party_type']

@admin.register(EnterpriseGroup)
class EnterpriseGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_head_name', 'group_nationality']
    search_fields = ['group_head__name', 'group_nationality']
    list_filter = ['group_nationality']
    autocomplete_fields = ['group_head']

    def group_head_name(self, obj):
        return obj.group_head.name
    group_head_name.admin_order_field = 'group_head__name'



@admin.register(PhysicalPerson)
class PhysicalPersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'physical_person_name', 'identification_number']
    search_fields = ['party__name', 'identification_number']
    autocomplete_fields = ['party']

    def physical_person_name(self, obj):
        return obj.party.name
    physical_person_name.admin_order_field = 'party__name'


@admin.register(LegalPerson)
class LegalPersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'legal_person_name', 'registry_code', 'foreign_code', 'foreign_country_code']
    search_fields = ['party__name', 'registry_code', 'foreign_code', 'foreign_country_code']
    autocomplete_fields = ['party']

    def legal_person_name(self, obj):
        return obj.party.name
    legal_person_name.admin_order_field = 'party__name'


@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ['id', 'legal_person_name', 'assets_value']
    search_fields = ['legal_person__party__name', 'legal_person__registry_code']
    autocomplete_fields = ['legal_person']

    def legal_person_name(self, obj):
        return obj.legal_person.party.name
    legal_person_name.admin_order_field = 'legal_person__party__name'


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'child_party_name', 'parent_party', 'share_percentage', 'enterprise_group_name']
    search_fields = ['child_party__name', 'parent_party__name', 'enterprise_group__group_head__name']
    autocomplete_fields = ['child_party', 'parent_party', 'enterprise_group']

    def child_party_name(self, obj):
        return obj.child_party.name
    child_party_name.admin_order_field = 'child_party__name'

    def parent_party_name(self, obj):
        return obj.parent_party.name
    parent_party_name.admin_order_field = 'parent_party__name'

    def enterprise_group_name(self, obj):
        if obj.enterprise_group is None:
            return None
        return obj.enterprise_group.group_head.name
    enterprise_group_name.admin_order_field = 'enterprise_group__group_head__name'
import pgtrigger
from django.db import models


class Party(models.Model):
    # Allowed values: J - Enterprise, F - Physical person
    party_type = models.CharField(max_length=1, choices=[('J', 'Enterprise'), ('F', 'Physical person')])
    name = models.CharField(max_length=1000, blank=True, null=True)
    party_uniq_key = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"({self.party_type}) {self.name}"


class Ownership(models.Model):
    parent_party = models.ForeignKey(Party, on_delete=models.SET_NULL, blank=True, null=True)
    child_party = models.ForeignKey(Party, on_delete=models.SET_NULL, related_name="ownerships", blank=True, null=True)
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    enterprise_group = models.ForeignKey('EnterpriseGroup', on_delete=models.SET_NULL, blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)


class EnterpriseGroup(models.Model):
    group_head = models.ForeignKey(Party, on_delete=models.CASCADE, blank=True, null=True, related_name="enterprise_group_heads")
    group_nationality = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"{self.group_head}"


class PhysicalPerson(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=200, blank=True, null=True)


class LegalPerson(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    registry_code = models.CharField(max_length=20, blank=True, null=True)
    foreign_code = models.CharField(max_length=100, blank=True, null=True)
    foreign_country_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"{self.party.name} ({self.registry_code})"


class Assets(models.Model):
    legal_person = models.ForeignKey(LegalPerson, on_delete=models.CASCADE)
    assets_value = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)


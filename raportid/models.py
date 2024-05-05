from django.db import models

from data_storage.models import Party


# Create your models here.
class EnterpriseGroups(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    assets_value = models.DecimalField(max_digits=20, decimal_places=2)
    enterprise = models.ForeignKey(Party, models.DO_NOTHING)

    class Meta:
        managed = False

    def __str__(self):
        return self.name


class Enterprises(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(EnterpriseGroups, models.DO_NOTHING)
    assets_value = models.DecimalField(max_digits=20, decimal_places=2)
    share_percentage = models.DecimalField(max_digits=20, decimal_places=2)
    owner = models.ForeignKey(Party, models.DO_NOTHING)

    class Meta:
        managed = False

    def __str__(self):
        return self.name

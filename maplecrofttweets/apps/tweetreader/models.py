from django.db import models
from django.db.models import Q


class CountryManager(models.Manager):
    """New class CountryManager."""

    def only_with_coordinates(self, *args, **kwargs):
        """Return only with lat and lng"""
        return self.get_queryset().filter(
            Q(lat__isnull=False) | Q(lng__isnull=False))


class Country(models.Model):
    """New class Country."""
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    objects = CountryManager()

    class Meta(object):
        """New class Meta."""
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

from django.contrib import admin

from apps.tweetreader.models import Country


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')
    list_display = ('pk', 'name', 'code', 'lat', 'lng')


admin.site.register(Country, CountryAdmin)

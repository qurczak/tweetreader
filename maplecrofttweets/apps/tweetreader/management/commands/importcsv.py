import logging

import csv

import os
from apps.tweetreader.models import Country

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


def convert_to_float(value):
    """Convert to float. In some records is 'None' on lat or lng position"""
    try:
        # No verification if numeric range is on Earth
        return float(value)
    except ValueError:
        return None


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--filename', action="store", type=str,
                            help='CSV filename')

    @transaction.atomic
    def import_countries(self, filename):
        # name, code, lng, lat
        expected_header = ['', '', 'lng', 'lat']

        with open(filename) as csvfile:
            country_reader = csv.reader(csvfile)
            header = next(country_reader)
            if header != expected_header:
                raise CommandError('Invalid header in CSV file')

            # DELETE ALL
            Country.objects.all().delete()

            num, total = 0, 0
            for row in country_reader:
                total += 1
                if len(row) != 4:
                    # Ignore empty
                    print("Problem with: {}", row)
                    continue

                country = Country(
                    name=row[0],
                    code=row[1],
                    lat=convert_to_float(row[2]),
                    lng=convert_to_float(row[3])
                )
                country.save()
                num += 1
            print('Imported {} records of {}'.format(num, total))

    def handle(self, *args, **options):
        filename = options['filename']
        if not filename:
            raise CommandError('--filename not set')
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            raise CommandError('Invalid filename {}'.format(filename))

        self.import_countries(filename)

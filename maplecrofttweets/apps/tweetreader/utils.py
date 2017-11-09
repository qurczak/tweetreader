import re
import tweepy
from apps.tweetreader.models import Country
from django.conf import settings
from django.core.cache import cache
from functools import wraps
from tweepy.error import TweepError


def mycache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        def inner():
            return f(*args, **kwargs)

        return cache.get_or_set(repr(f), inner)  # Replace repr() with sha1()

    return wrapper


class SearchCountries(object):
    """New class SearchCountries."""

    _country_rx = None

    @staticmethod
    def filter_for_tags(line):
        """Return possible countries in specific line"""
        return [x[1:] for x in line.split() if x.startswith('#')]

    @staticmethod
    @mycache
    def get_country_by_name(name):
        """For caching."""
        try:
            return Country.objects.only_with_coordinates().get(name=name)
        except Country.DoesNotExist:
            return None

    @staticmethod
    @mycache
    def get_country_by_pk(pk):
        """For caching."""
        try:
            return Country.objects.only_with_coordinates().get(pk=pk)
        except Country.DoesNotExist:
            return None

    @mycache
    def countries_tags(self):
        """Convert to dict and change name: 'Saudi Arabia' -> 'SaudiArabia'.
        Keep pk to find real name.

        :rtype: dict
        """
        data = list(
            Country.objects.only_with_coordinates().values_list('name', 'pk'))
        return dict(
            {(name.replace(' ', ''), pk) for name, pk in data})

    @mycache
    def countries_names(self):
        """Get all countries."""
        return list(Country.objects.only_with_coordinates()
                    .only('name').values_list('name', flat=True))

    def search_for_countries(self, lines):
        """Search for all countries"""
        countries_found = set()
        for line in lines:
            countries_found.update(self.by_tags(line))
            countries_found.update(self.by_text(line))
            countries_found.update(self.by_regexp(line))
        return countries_found

    def by_tags(self, line):
        """Find by tags"""
        data = self.filter_for_tags(line)
        countries = set(self.countries_tags().keys()) & set(data)
        countries = {self.get_country_by_pk(self.countries_tags()[name]) for name in countries}
        return countries or {}

    def by_text(self, line):
        """Find country based on words"""
        data = set(line.split())
        countries = set(self.countries_names()) & set(data)
        countries = {self.get_country_by_name(name) for name in countries}
        return countries or {}

    def by_regexp(self, line):
        """Find Nigeria's and unmatched by regexp"""
        escaped = [re.escape(x) for x in self.countries_names()]
        if not self._country_rx:
            # The compilation takes a long time
            self._country_rx = re.compile('({})'.format('|'.join(escaped)))
        data = [self.get_country_by_name(name)
                for name in self._country_rx.findall(line)]
        # Filter non empty
        return {_ for _ in data if _}


def get_twitter_api():
    """Twitter api."""
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def get_data_from_user(name, tweet_count=30):
    """Get data."""
    api = get_twitter_api()
    try:
        tweets = api.user_timeline(id=name, count=tweet_count)
    except TweepError as exc:
        print('Exception: {}'.format(exc))
        return []
    else:
        return [tweet.text for tweet in tweets]

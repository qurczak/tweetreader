from apps.tweetreader.utils import get_data_from_user, SearchCountries
from django.shortcuts import render


def tweets(request):
    user_tweets = get_data_from_user("maplecroftrisk")
    search_countries = SearchCountries()
    locations = search_countries.search_for_countries(user_tweets)
    context = {
        'user_tweets': user_tweets,
        'locations': locations}
    return render(request, 'tweets.html', context)

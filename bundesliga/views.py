from webbrowser import get
from django.shortcuts import render
import requests

from datetime import date

from .utils import set_datetime, filter_teams
# Create your views here.


def home(request):
    # Gets the value passed to the search field
    get_team = request.GET.get('teams')

    current_year = date.today().year
    matches = requests.get(
        f'https://www.openligadb.de/api/getmatchdata/bl1/{current_year}').json()

    """
    In the first half of coming year the link above will be empty, because it will try to get the data for the next season.
    When that's case the current year gets decremented to the previous year to get the ongoing season.
    When the ongoing season ends the above link will not be empty anymore and return the new season.
    """
    if not matches:
        matches = requests.get(
            f'https://www.openligadb.de/api/getmatchdata/bl1/{current_year - 1}').json()

    set_datetime(matches)

    if get_team:
        matches = filter_teams(get_team, matches)

    context = {
        'matches': matches,
    }
    return render(request, 'bundesliga/home.html', context)


def upcoming_matches(request):
    get_team = request.GET.get('teams')

    teams_data = requests.get(
        'https://www.openligadb.de/api/getmatchdata/bl1').json()
    current_gameday = requests.get(
        'https://www.openligadb.de/api/getcurrentgroup/bl1').json()

    set_datetime(teams_data)

    if get_team:
        teams_data = filter_teams(get_team, teams_data)

    context = {
        'teams': teams_data,
        'current_gameday': current_gameday,
    }
    return render(request, 'bundesliga/upcoming.html', context)


def team_stats(request):
    get_team = request.GET.get('teams')
    current_year = date.today().year

    stats = requests.get(
        f'https://www.openligadb.de/api/getbltable/bl1/{current_year}').json()

    if not stats:
        stats = requests.get(
            f'https://www.openligadb.de/api/getbltable/bl1/{current_year - 1}').json()

    if get_team:
        stats = [x for x in stats if get_team.lower() in x['TeamName'].lower()]

    context = {
        'stats': stats,
    }
    return render(request, 'bundesliga/stats.html', context)

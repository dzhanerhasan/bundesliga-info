from datetime import datetime


def set_datetime(data):
    # Change datetime from the API to a more readable format.
    for team in data:
        match_datetime = team['MatchDateTime']
        match_time_obj = datetime.strptime(
            match_datetime, '%Y-%m-%dT%H:%M:%S')

        team['match_time'] = match_time_obj.time()
        team['match_date'] = match_time_obj.date()


def filter_teams(name, data):
    """
    If the value in the search field is not empty, displays only the teams that correspond to the value of the 'get_team' variable.
    E.g. If the value is 'FC', displays only the teams that have 'FC' in their names, etc.
    """

    data = [x for x in data
            if name.lower() in x['Team1']['TeamName'].lower()
            or name.lower() in x['Team2']['TeamName'].lower()]

    return data

from django.shortcuts import render
import requests
import datetime
import pytz
from tzlocal import get_localzone
import json


# Create your views here.

# Function to get and process request and response
def get_match_data(request):
    # Your API_KEY
    api_key = "f1a32bca650c34dd940b273814110fe4082c4067d954486ae56d9bf502ff2458"

    # Querystring data recheived via a form in match.html
    # league_id,from_date and to_date
    if request.method == "POST":
        league_id = request.POST.get('league_id')
    else :
        league_id = 62

    if request.method == "POST":
        from_date = request.POST.get('from_date')

    else:
        from_date = datetime.datetime.now().date()

    if request.method == "POST":
        to_date = request.POST.get('to_date')

    else:
        to_date = datetime.datetime.now().date()


    # Requel URl, Querystring, Request headers
    url = "https://apifootball.com/api/"

    querystring = {"action":"get_events",'league_id':league_id,"from":from_date,"to":to_date,"APIkey":api_key}

    payload = ""
    headers = {
        'Authorization': "Basic c2hpZmFuOg==",
        'cache-control': "no-cache",
        'Postman-Token': "7e0a735b-3622-4bc7-a4dd-a66f97a2392d"
        }

    # Response data and it's formating into json

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = response.json()
    length = len(response)

    match_data = []
    match_error = {}

    try:
        for i in range(length):
             match = {
                'match_id' : response[i]['match_id'],
                'match_status' : response[i]['match_status'],
                'match_date' : date_format(response[i]['match_date']),
                'match_time' : time_format(response[i]['match_date'],response[i]['match_time']),
                'home_team' : response[i]['match_hometeam_name'],
                'home_team_score' : response[i]['match_hometeam_score'],
                'away_team' : response[i]['match_awayteam_name'],
                'away_team_score' : response[i]['match_awayteam_score']

             }

             match_data.append(match)

    except:
        match_error = {
            'message' : response['message']
        }

    querystring = {"action":"get_leagues","APIkey":api_key}

    payload = ""
    headers = {
        'Authorization': "Basic c2hpZmFuOg==",
        'cache-control': "no-cache",
        'Postman-Token': "ac7ecc21-6911-4741-af3e-7411c01b8a9c"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = response.json()
    length = len(response)

    competitions = []

    for i in range(length):
         league_details = {
            'league_id':response[i]['league_id'],
            'league_name':response[i]['league_name']
         }
         competitions.append(league_details)

    return render(request, 'match.html', context={'match_data':match_data,'match_error':match_error, 'competitions':competitions})



# Get specific match details
def match_details(request, match_id):
    url = "https://apifootball.com/api/"

    querystring = {"action":"get_events","match_id":match_id,"APIkey":"f1a32bca650c34dd940b273814110fe4082c4067d954486ae56d9bf502ff2458"}

    payload = ""
    headers = {
        'Authorization': "Basic c2hpZmFuOg==",
        'cache-control': "no-cache",
        'Postman-Token': "ac7ecc21-6911-4741-af3e-7411c01b8a9c"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = response.json()
    length = len(response)


    # Populating Match Overview Information
    match_info = {
        "match_id": response [0]['match_id'],
        "country_id": response [0]['country_id'],
        "country_name": response [0]['country_name'],
        "league_id": response [0]['league_id'],
        "league_name": response [0]['league_name'],
        "match_date": date_format(response [0]['match_date']),
        "match_status":status_format(response [0]['match_status']),
        "match_time":time_format(response [0]['match_date'],response [0]['match_time']),
        "match_hometeam_name":response [0]['match_hometeam_name'],
        "match_hometeam_score":response [0]['match_hometeam_score'],
        "match_awayteam_name":response [0]['match_awayteam_name'],
        "match_awayteam_score":response [0]['match_awayteam_score'],
        "match_hometeam_halftime_score":response [0]['match_hometeam_halftime_score'],
        "match_awayteam_halftime_score": response [0]['match_awayteam_halftime_score'],
        "match_hometeam_extra_score":response [0]['match_hometeam_extra_score'],
        "match_awayteam_extra_score":response [0]['match_awayteam_extra_score'],
        "match_hometeam_penalty_score":response [0]['match_hometeam_penalty_score'],
        "match_awayteam_penalty_score": response [0]['match_awayteam_penalty_score'],
        "match_hometeam_system": response [0]['match_hometeam_system'],
        "match_awayteam_system": response [0]['match_awayteam_system'],
        "match_live": response [0]['match_live'],

    }

    # Setting up home team player postion in row according to team format
    match_home_row = {}
    try:
        match_home_format = match_info['match_hometeam_system'].split('-')
        match_home_row = {
        'one' : str(int(match_home_format[0]) + 1),
        'two': str(int(match_home_format[0]) + 1 + int(match_home_format [1]))
        }
    except:
        print("Hello World!")

    # Setting up away team player postion in row according to team format
    match_away_row = {}
    try:
        match_away_format = match_info['match_awayteam_system'].split('-')

        match_away_row = {
        'one' : str((11-int(match_away_format[2]))+1),
        'two': str(11-(int(match_away_format[2])+int(match_away_format[1]))+1),
        'three':str(11-(int(match_away_format[2])+int(match_away_format[1])+int(match_away_format[0]))+1),
        }
    except:
        print("Hello World!")



    # Populating Goalscorer Information
    length = len(response[0]['goalscorer'])
    goalscorer = []

    for i in range(length):
        scorer = {
         "time": response[0]['goalscorer'][i]['time'],
         "home_scorer":response[0]['goalscorer'][i]['home_scorer'],
         "score": response[0]['goalscorer'][i]['score'],
         "away_scorer": response[0]['goalscorer'][i]['away_scorer']

        }
        goalscorer.append(scorer)


    events = []

    player_ins = []
    player_outs = []
    # Populating timeline
    timeline=["1'","2'","3'","4'","5'","6'","7'","8'","9'","10'","11'","12'","13'","14'","15'","16'","17'","18'","19'","20'","21'","22'","23'","24'","25'","26'","27'","28'","29'","30'","31'","32'","33'","34'","35'","36'","37'","38'","39'","40'","41'","42'","43'","44'","45'","46'","47'","48'","49'","50'","51'","52'","53'","54'","55'","56'","57'","58'","59'","60'","61'","62'","63'","64'","65'","66'","67'","68'","69'","70'","71'","72'","73'","74'","75'","76'","77'","78'","79'","80'","81'","82'","83'","84'","85'","86'","87'","88'","89'","90'","91'","92'","93'","94'","95'","96'"] # time upto 96 , miniutes
    for i in range(len(timeline)):
        if timeline[i] == "45'":
                event = {
                "time": "45'",
                "score": match_info['match_hometeam_halftime_score'] + "-" + match_info['match_awayteam_halftime_score'],
                }
                events.append(event)

        for j in range(len(response[0]['cards'])):
            if timeline[i] == response[0]['cards'][j]['time']:

                event = {
                'type':'card',
                "time": response[0]['cards'][j]['time'],
                "home_fault":response[0]['cards'][j]['home_fault'],
                "card": response[0]['cards'][j]['card'],
                "away_fault":response[0]['cards'][j]['away_fault']

                }
                events.append(event)


        for k in range(len(response[0]['goalscorer'])):
            if timeline[i] == response[0]['goalscorer'][k]['time']:

                event = {
                'type':'goal',
                "time": response[0]['goalscorer'][k]['time'],
                "home_scorer":response[0]['goalscorer'][k]['home_scorer'],
                "score": response[0]['goalscorer'][k]['score'],
                "away_scorer": response[0]['goalscorer'][k]['away_scorer']
                }
                events.append(event)

        for l in range(len(response[0]['lineup']['home']['substitutions'])):
            if timeline[i] == response[0]['lineup']['home']['substitutions'][l]['lineup_time']:

                event = {
                'type':'substitution',
                "lineup_player_in":player_in(response[0]['lineup']['home']['substitutions'][l]['lineup_player']),
                "lineup_player_out":player_out(response[0]['lineup']['home']['substitutions'][l]['lineup_player']),
                "lineup_number": response[0]['lineup']['home']['substitutions'][l]['lineup_number'],
                "lineup_position":response[0]['lineup']['home']['substitutions'][l]['lineup_position'],
                "time":response[0]['lineup']['home']['substitutions'][l]['lineup_time'],
                "team_name":match_info['match_hometeam_name']
                }
                events.append(event)
                player_ins.append(event['lineup_player_in'])
                player_outs.append(event['lineup_player_out'])


        for m in range(len(response[0]['lineup']['away']['substitutions'])):
            if timeline[i] == response[0]['lineup']['away']['substitutions'][m]['lineup_time']:

                event = {
                'type':'substitution',
                "lineup_player_in":player_in(response[0]['lineup']['away']['substitutions'][m]['lineup_player']),
                "lineup_player_out":player_out(response[0]['lineup']['away']['substitutions'][m]['lineup_player']),
                "lineup_number": response[0]['lineup']['away']['substitutions'][m]['lineup_number'],
                "lineup_position":response[0]['lineup']['away']['substitutions'][m]['lineup_position'],
                "time":response[0]['lineup']['away']['substitutions'][m]['lineup_time'],
                "team_name":match_info['match_awayteam_name']
                }
                events.append(event)
                player_ins.append(event['lineup_player_in'])
                player_outs.append(event['lineup_player_out'])

    events.reverse()

    # Saving player list as String
    player_outs=player_subs_format(player_outs)
    player_ins =player_subs_format(player_ins)

    # Populating Starting Lineup for home team
    length = len(response[0]['lineup']['home']['starting_lineups'])
    lineup_home_starting = []

    for i in range(length):
        lineup_home_start = {
         "lineup_player": response[0]['lineup']['home']['starting_lineups'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['home']['starting_lineups'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['home']['starting_lineups'][i]['lineup_position']
        }
        lineup_home_starting.append(lineup_home_start)


    # Populating Substitutes Lineup for home team
    length = len(response[0]['lineup']['home']['substitutes'])
    lineup_home_substitutes = []

    for i in range(length):
        lineup_home_subs = {
         "lineup_player": player_in(response[0]['lineup']['home']['substitutes'][i]['lineup_player']),
         "lineup_number": response[0]['lineup']['home']['substitutes'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['home']['substitutes'][i]['lineup_position']
        }
        lineup_home_substitutes.append(lineup_home_subs)

    # Populating Coach/Manager Lineup for home team
    home_manager = ""
    try:
        home_manager = response[0]['lineup']['home']['coach'][0]
    except:
        print("Hello World!")

    # Populating Starting Lineup for away team
    length = len(response[0]['lineup']['away']['starting_lineups'])
    lineup_away_starting = []

    for i in range(length):
        lineup_away_start = {
         "lineup_player": response[0]['lineup']['away']['starting_lineups'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['away']['starting_lineups'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['away']['starting_lineups'][i]['lineup_position']
        }
        lineup_away_starting.append(lineup_away_start)


    # Populating Substitutes Lineup for away team
    length = len(response[0]['lineup']['away']['substitutes'])
    lineup_away_substitutes = []

    for i in range(length):
        lineup_away_subs = {
         "lineup_player": player_in(response[0]['lineup']['away']['substitutes'][i]['lineup_player']),
         "lineup_number": response[0]['lineup']['away']['substitutes'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['away']['substitutes'][i]['lineup_position']
        }
        lineup_away_substitutes.append(lineup_away_subs)

    # Populating Coach/Manager Lineup for away team
    away_manager = ""
    try:
        away_manager = response[0]['lineup']['away']['coach'][0]
    except:
        print("Hello World!")


    # Populating Statistics
    length = len(response[0]['statistics'])
    statistics = []

    for i in range(length):
        stats = {
         "type": response[0]['statistics'][i]['type'],
         "home": response[0]['statistics'][i]['home'],
         "away": response[0]['statistics'][i]['away']
        }
        statistics.append(stats)


    return render(request, 'match-details.html', context={'match_info':match_info, 'goalscorer':goalscorer,  'lineup_home_starting':lineup_home_starting,'lineup_home_substitutes':lineup_home_substitutes,'home_manager':home_manager,'lineup_away_starting':lineup_away_starting,'lineup_away_substitutes':lineup_away_substitutes,'away_manager':away_manager,'statistics':statistics,'match_home_row':match_home_row,'match_away_row':match_away_row,'events':events, 'player_ins':player_ins, 'player_outs':player_outs})


# Converting json date string to custom date format
def date_format(date):

    temp_date = date.split('-')

    year = int(temp_date[0])
    month = int(temp_date [1])
    day = int(temp_date [2])

    if day == datetime.datetime.now().date().day :
        return "Today"
    elif is_next_day(day):
         return "Tommorow"
    else:
        return week_day(year,month,day) + "," +str(month) +"/"+ str(day) # have to work here

# Converting json time string to custom time format
def time_format(date, time):
    if time == 'Postp.':
        return "Time TBD"
    else:
        temp_date = date.split('-')
        year = int(temp_date[0])
        month = int(temp_date [1])
        day = int(temp_date [2])

        temp_time = time.split(':')
        hour = int(temp_time [0])
        minutes = int(temp_time[1])

        temp_dt = datetime.datetime(year,month,day,hour,minutes,10)
        temp_dt_utc = temp_dt.replace(tzinfo=pytz.UTC)
        tz_local = get_localzone()
        local_dt = temp_dt_utc.astimezone(tz_local)

        hour = local_dt.hour
        minutes = local_dt.minute

        if minutes < 10:
            minutes = str(minutes)
            minutes = "0" + minutes
        else:
            minutes = str(minutes)
        ap = "AM"

        if hour >= 12 and hour <= 23:
            ap = "PM"

        if hour > 12:
            hour = hour%12

        return str(hour) + ":" + minutes + " " + ap



# output player list as string
def player_subs_format(player_list):
    output = ""
    for player in player_list:
        output += "'" + player + "'" + ","
    return output


#determine which player in or out
def player_in(player):
    try:
        temp_player = player.split('|')
        return temp_player [1]
    except:
        return player


def player_out(player):
    temp_player = player.split('|')
    return temp_player [0]

# Formating match status
def status_format(status):
    if status == "FT":
        return "Full Time"
    else:
        return status

# Tell if a given day is next_day of today
def is_next_day(day):

    today = int(datetime.datetime.now().date().day)
    month = int(datetime.datetime.now().date().month)
    year = int(datetime.datetime.now().date().year)


    days_31 = [1,3,5,7,8,10,12]
    days_30 = [4,6,9,11]

    if day == 1 :
        if (month in days_30 and today == 30) or (month in days_31 and today ==31):
            return True
        elif month == 2:
            if is_leap_year(year) and today == 29:
                return True
            elif today == 28:
                return True

    elif day == today + 1:
        return True

# check wheare the given year is leap year or not
def is_leap_year(year):
    if year % 100 == 0 :
        if year % 400 == 0:
            return True
    elif year % 4 == 0:
                return True;
    else:
        return False

# Find day of week.modified from stackoverflow
def week_day(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    week   = ['Sun',
              'Mon',
              'Tues',
              'Wed',
              'Thurs',
              'Fri',
              'Sat']
    after_feb = 1
    if month > 2: after_feb = 0
    aux = year - 1700 - after_feb
    # dayOfWeek for 1700/1/1 = 5, Friday
    day_of_week  = 5
    # partial sum of days betweem current date and 1700/1/1
    day_of_week += (aux + after_feb) * 365
    # leap year correction
    day_of_week += aux / 4 - aux / 100 + (aux + 100) / 400
    # sum monthly and day offsets
    day_of_week += offset[month - 1] + (day - 1)
    day_of_week %= 7
    return week[int(day_of_week)]

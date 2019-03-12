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
    api_key = "679b57ce04028d0c3b6d5b1263c48e545ee123234cd101a97397c72ec88daa1b"

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

    querystring = {"action":"get_events","match_id":match_id,"APIkey":"679b57ce04028d0c3b6d5b1263c48e545ee123234cd101a97397c72ec88daa1b"}

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
    match_home_format = match_info['match_hometeam_system'].split('-')
    match_home_row = {
    'one' : str(int(match_home_format[0]) + 1),
    'two': str(int(match_home_format[0]) + 1 + int(match_home_format [1]))
    }

    # Setting up away team player postion in row according to team format
    match_away_format = match_info['match_awayteam_system'].split('-')

    match_away_row = {
    'one' : str((11-int(match_away_format[2]))+1),
    'two': str(11-(int(match_away_format[2])+int(match_away_format[1]))+1),
    'three':str(11-(int(match_away_format[2])+int(match_away_format[1])+int(match_away_format[0]))+1),
    }



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

    # Populating Match faul card Information
    length = len(response[0]['cards'])
    cards = []

    for i in range(length):
        card = {
        "time": response[0]['cards'][i]['time'],
        "home_fault":response[0]['cards'][i]['home_fault'],
        "card": response[0]['cards'][i]['card'],
        "away_fault":response[0]['cards'][i]['away_fault']

        }
        cards.append(card)

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
         "lineup_player": response[0]['lineup']['home']['substitutes'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['home']['substitutes'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['home']['substitutes'][i]['lineup_position']
        }
        lineup_home_substitutes.append(lineup_home_subs)

    # Populating Coach/Manager Lineup for home team
    home_manager = response[0]['lineup']['home']['coach'][0]

    # Populating Substitutions Lineup for home team
    length = len(response[0]['lineup']['home']['substitutions'])
    lineup_home_substitutions = []

    for i in range(length):
        lineup_home_subs = {
         "lineup_player": response[0]['lineup']['home']['substitutions'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['home']['substitutions'][i]['lineup_number'],
         "lineup_position":response[0]['lineup']['home']['substitutions'][i]['lineup_position'],
         "lineup_time":response[0]['lineup']['home']['substitutions'][i]['lineup_time']
        }
        lineup_home_substitutions.append(lineup_home_subs)

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
         "lineup_player": response[0]['lineup']['away']['substitutes'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['away']['substitutes'][i]['lineup_number'],
         "lineup_position": response[0]['lineup']['away']['substitutes'][i]['lineup_position']
        }
        lineup_away_substitutes.append(lineup_away_subs)

    # Populating Coach/Manager Lineup for away team
    away_manager = response[0]['lineup']['away']['coach'][0]

    # Populating Substitutions Lineup for away team
    length = len(response[0]['lineup']['away']['substitutions'])
    lineup_away_substitutions = []

    for i in range(length):
        lineup_away_subs = {
         "lineup_player": response[0]['lineup']['away']['substitutions'][i]['lineup_player'],
         "lineup_number": response[0]['lineup']['away']['substitutions'][i]['lineup_number'],
         "lineup_position":response[0]['lineup']['away']['substitutions'][i]['lineup_position'],
         "lineup_time":response[0]['lineup']['away']['substitutions'][i]['lineup_time']
        }
        lineup_away_substitutions.append(lineup_away_subs)

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

    return render(request, 'match-details.html', context={'match_info':match_info, 'goalscorer':goalscorer, 'cards':cards, 'lineup_home_starting':lineup_home_starting,'lineup_home_substitutes':lineup_home_substitutes,'home_manager':home_manager,'lineup_home_substitutions':lineup_home_substitutions,'lineup_away_starting':lineup_away_starting,'lineup_away_substitutes':lineup_away_substitutes,'away_manager':away_manager,'lineup_away_substitutions':lineup_away_substitutions,'statistics':statistics,'match_home_row':match_home_row,'match_away_row':match_away_row})


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
        return weekDay(year,month,day) + "," +str(month) +"/"+ str(day) # have to work here

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
        print(temp_dt_utc)
        print(local_dt)

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

# Find day of week
def weekDay(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    week   = ['Sun',
              'Mon',
              'Tues',
              'Wed',
              'Thurs',
              'Fri',
              'Sat']
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    # dayOfWeek for 1700/1/1 = 5, Friday
    dayOfWeek  = 5
    # partial sum of days betweem current date and 1700/1/1
    dayOfWeek += (aux + afterFeb) * 365
    # leap year correction
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
    # sum monthly and day offsets
    dayOfWeek += offset[month - 1] + (day - 1)
    dayOfWeek %= 7
    return week[int(dayOfWeek)]

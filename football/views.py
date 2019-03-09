from django.shortcuts import render
import requests
import datetime
from django.utils import timezone


# Create your views here.

# Api data
def get_api_data(request):

    api_key = "679b57ce04028d0c3b6d5b1263c48e545ee123234cd101a97397c72ec88daa1b"

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


    url = "https://apifootball.com/api/"

    querystring = {"action":"get_events",'league_id':league_id,"from":from_date,"to":to_date,"APIkey":api_key}

    payload = ""
    headers = {
        'Authorization': "Basic c2hpZmFuOg==",
        'cache-control': "no-cache",
        'Postman-Token': "7e0a735b-3622-4bc7-a4dd-a66f97a2392d"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = response.json()
    length = len(response)

    match_data = []

    for i in range(length):
         match = {
            'match_id' : response[i]['match_id'],
            'match_status' : response[i]['match_status'],
            'match_date' : date_format(response[i]['match_date']),
            'match_time' : time_format(response[i]['match_time']),
            'home_team' : response[i]['match_hometeam_name'],
            'home_team_score' : response[i]['match_hometeam_score'],
            'away_team' : response[i]['match_awayteam_name'],
            'away_team_score' : response[i]['match_awayteam_score']

         }
         match_data.append(match)

    return render(request, 'api.html', context={'match_data':match_data})


# Converting json date string to custom date format
def date_format(date):

    temp_date = date.split('-')
    day = int(temp_date [2])
    month = int(temp_date [1])

    if day == datetime.datetime.now().date().day :
        return "Today"
    elif is_next_day(day):
         return "Tommorow"
    else:
        return temp_date # have to work here

# Converting json time string to custom time format
def time_format(time):
    if time == 'Postp.':
        return "Time TBD"
    else:
        temp_time = time.split(':')
        hour = int(temp_time [0]) + 6 # have to work here. time should be in current timezone
        minutes = int(temp_time[1])
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

def is_leap_year(year):
    if year % 4 == 0 : 
        return True;
    else:
        return False

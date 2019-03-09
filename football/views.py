from django.shortcuts import render
import requests
import datetime

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
    # elif day > datetime.datetime.now().date().day :
    #     return "Tommorow"

    else:
        print(day)
        return temp_date

# Converting json time string to custom time format
def time_format(time):
    temp_time = time.split(':')
    hour = int(temp_time [0]) + 6
    minutes = int(temp_time[1])
    ap = "AM"

    if hour >= 12 and hour <= 23:
        ap = "PM"

    if hour > 12:
        hour = hour%12

    return str(hour) + ":" + str(minutes) + " " + ap

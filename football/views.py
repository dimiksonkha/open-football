from django.shortcuts import render
import requests
import datetime
import pytz
from tzlocal import get_localzone


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

    return render(request, 'match.html', context={'match_data':match_data})


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

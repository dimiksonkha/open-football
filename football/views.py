from django.shortcuts import render
import requests

# Create your views here.

# Api data
def get_api_data(request):

        url = "http://api.football-data.org/v2/competitions/"

        payload = ""
        headers = {
            'Authorization': "Basic c2hpZmFuOjlhZjA2NTE3NTg5NDQ5OTI5MWY2MGYyYTE5YTk0NzY5",
            'cache-control': "no-cache",
            'Postman-Token': "3cce3742-3a75-41c5-a1c3-0c35f1cb5d1a"
            }

        response = requests.request("GET", url, data=payload, headers=headers)
        response = response.json()
        response = response ['competitions'][0]['area']

        print(response)
        my_dict = {'response':response}
        return render(request, 'api.html', context=my_dict)

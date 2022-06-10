from django.shortcuts import redirect, render, get_object_or_404
from decouple import config
import requests
from pprint import pprint
from weatherapp.models import City
from django.contrib import messages

def home(request):
    #city_name = 'Amsterdam'
    API_key = config('API_KEY')
    user_city = request.GET.get('name')


    if user_city:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API_key}&units=metric'
        response = requests.get(url)
        if response.ok: #if response.status_code == 200:
            content = response.json()
            response_city = content["name"]
            if City.objects.filter(name=response_city):
                messages.warning(request, 'City already exists!')
            else:
                City.objects.create(name=response_city)
                messages.success(request, 'City successfully created!')
        else:
            messages.warning(request, "City name not found!")      
        return redirect('home')      

    #Creating an empty list before and use append method to add things
    city_data = []
    cities = City.objects.all()

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        #first get the data with requests module
        response = requests.get(url)
        # Use json() method to convert incoming JSON data to a python dictionary.
        content = response.json()

        data = {
            'city' : city,
            'temp' : content.get('main').get('temp'),
            'desc' : content['weather'][0]['description'],
            'icon' : content['weather'][0]['icon']
        }
        city_data.append(data)
        pprint(city_data)

    context = {
        'city_data' : city_data,
    } 
    return render(request, "weatherapp/home.html", context)

def delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, 'City deleted')
    return redirect('home')

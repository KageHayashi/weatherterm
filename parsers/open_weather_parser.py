import re
import os
import requests
import json

from dotenv import load_dotenv

from weatherterm.core import ForecastType
from weatherterm.core import Forecast
from weatherterm.core import Request
from weatherterm.core import Unit
from weatherterm.core import UnitConverter

load_dotenv()

class OpenWeatherParser:
    '''
    A parser for the OpenWeather API
    '''
    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.FIVEDAYS: self._five_and_ten_days_forecast,
            ForecastType.TENDAYS: self._five_and_ten_days_forecast,
            ForecastType.WEEKEND: self._weekend_forecast,
            }

        self._api_key = os.getenv('OPEN_WEATHER_API_KEY')
        self._base_url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        # OpenWeather API gives weather in kelvins by default
        self._unit_converter = UnitConverter(Unit.KELVIN)

    def _today_forecast(self, args):
        '''
        Return forecast for today
        '''
        # Retrieve data
        data = self._request(args)
        cur_temp = data['main']['temp']
        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        h = data['main']['humidity']
        w = data['wind']['speed']
        feels_like = data['main']['feels_like']

        # Convert temperatures to preferred unit
        self._unit_converter.dest_unit = args.unit
        cur_temp = self._unit_converter.convert(cur_temp)
        min_temp = self._unit_converter.convert(min_temp)
        max_temp = self._unit_converter.convert(max_temp)
        feels_like = self._unit_converter.convert(feels_like)

        desc = f"Feels like {feels_like}"

        # Create and return forecast object
        forecast = Forecast(current_temp=cur_temp, humidity=h, wind=w, low_temp=min_temp, high_temp=max_temp, description=desc, temp_type=args.unit)

        return forecast

    def _five_and_ten_days_forecast(self, args):
        raise NotImplementedError()

    def _weekend_forecast(self, args):
        raise NotImplementedError()

    def _request(self, args):
        '''
        Makes requests to the API
        '''
        url = self._base_url.format(city=args.city, api_key=self._api_key)
        r = requests.get(url)
        if r.status_code == 404:
            error_message = json.loads(r.content.decode())["message"]
            raise Exception(error_message)

        data = json.loads(r.content.decode())
        
        return data

    def run(self, args):
        '''
        Get the forecast type and run appropriate function
        '''
        self._forecast_type = args.forecast_option
        forecast_function = self._forecast[args.forecast_option]
        return forecast_function(args)
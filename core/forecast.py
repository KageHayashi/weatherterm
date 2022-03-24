from datetime import date

from .unit import Unit
from .forecast_type import ForecastType


class Forecast:
    '''
    Forecast object to store weather report
    '''
    def __init__(
            self,
            current_temp,
            humidity,
            wind,
            high_temp=None,
            low_temp=None,
            description='',
            forecast_date=None,
            forecast_type=ForecastType.TODAY,
            temp_type=None):
        self._current_temp = current_temp
        self._high_temp = high_temp
        self._low_temp = low_temp
        self._humidity = humidity
        self._wind = wind
        self._description = description
        self._forecast_type = forecast_type
        self._temp_type = temp_type

        if forecast_date is None:
            self.forecast_date = date.today()
        else:
            self._forecast_date = forecast_date

    @property
    def forecast_date(self):
        return self._forecast_date

    @forecast_date.setter
    def forecast_date(self, forecast_date):
        self._forecast_date = forecast_date.strftime("%a %b %d")

    @property
    def current_temp(self):
        return self._current_temp

    @property
    def humidity(self):
        return self._humidity

    @property
    def wind(self):
        return self._wind

    @property
    def description(self):
        return self._description

    def __str__(self):
        '''
        A string representation of the weather forecast report
        '''
        temperature = None
        unit_type = str(self._temp_type.name)[0]
        offset = ' ' * 4

        if self._forecast_type == ForecastType.TODAY:
            temperature = (f' {offset}{self._current_temp}\xb0 {unit_type}\n'
                           f' {offset}High {self._high_temp}\xb0 {unit_type}/ '
                           f'Low {self._low_temp}\xb0 {unit_type}')
        else:
            temperature = (f'{offset}High {self._high_temp}\xb0 {unit_type}/ '
                           f'Low {self._low_temp}\xb0 {unit_type}')

        return (f'>>> {self.forecast_date}\n'
                f'{temperature}'
                f' ({self._description})\n'
                f' {offset}Wind: '
                f'{self._wind} / Humidity: {self._humidity}\n')

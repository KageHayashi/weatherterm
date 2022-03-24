from .unit import Unit

class UnitConverter:
    '''
    UnitConverter converts temperature from one unit type to another unit type
    '''
    def __init__(self, from_unit, dest_unit=None):
        self.from_unit = from_unit
        self.dest_unit = dest_unit
        self._convert_functions = {
            Unit.CELSIUS: self._to_celsius,
            Unit.FAHRENHEIT: self._to_fahrenheit,
            Unit.KELVIN: self._to_kelvin
        }

    def convert(self, temp):
        try:
            temperature = float(temp)
        except ValueError:
            return 0

        # Same from and destination unit, just return
        if (self.dest_unit == self.from_unit or
            self.dest_unit is None):
            return self._format_results(temperature)

        # Choose the appropriate convert function
        func = self._convert_functions[self.dest_unit]
        result = func(temperature)

        return self._format_results(result)

    def _format_results(self, value):
        return int(value) if value.is_integer() else f'{value:.1f}'

    def _to_celsius(self, temp):
        '''
        Converts a given temperature to celsius
        '''
        if self.from_unit == Unit["FAHRENHEIT"]:
            result = (temp - 32) * 5 / 9
        elif self.from_unit == Unit["KELVIN"]:
            result = temp - 273.15

        return result

    def _to_fahrenheit(self, temp):
        '''
        Converts a given temperature to fahrenheit
        '''
        if self.from_unit == Unit["CELSIUS"]:
            result = (temp * 9 / 5) + 32
        elif self.from_unit == Unit["KELVIN"]:
            result = (temp - 273.15) * 1.8 + 32

        return result

    def _to_kelvin(self, temp):
        '''
        Converts a given temperature to kelvin
        '''
        if self.from_unit == Unit["CELSIUS"]:
            result = temp + 273.15
        elif self.from_unit == Unit["FAHRENHEIT"]:
            result = (temp - 32) / 1.8 + 273.15

        return result

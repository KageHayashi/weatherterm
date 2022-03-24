from argparse import Action

from weatherterm.core import Unit

class SetUnitAction(Action):
    '''
    Action triggered when given the -u/--unit argument
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        if values == "C":
            unit = Unit["CELSIUS"]
        elif values == "K":
            unit = Unit["KELVIN"]
        elif values == "F":
            unit = Unit["FAHRENHEIT"]
        setattr(namespace, self.dest, unit)
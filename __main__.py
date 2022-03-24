import sys
from argparse import ArgumentParser

from weatherterm.core import parser_loader
from weatherterm.core import ForecastType
from weatherterm.core import Unit
from weatherterm.core import SetUnitAction

# Load parsers
parsers = parser_loader.load('./weatherterm/parsers')

# Load argument parser
argparser = ArgumentParser(
    prog='weatherterm',
    description='Weather info from weather.com on your terminal')

# Add required arguments
required = argparser.add_argument_group('required arguments')
unit_values = [name.title()[0] for name, _ in Unit.__members__.items()]

required.add_argument('-c', '--city',
  required=True,
  dest='city',
  metavar='city',
  help='ex. San Francisco, New York')

# Add optional arguments
argparser.add_argument('-p', '--parser',
  required=False,
  dest='parser',
  metavar='parser',
  choices=parsers,
  default='OpenWeatherParser',
  help='Specify a parser to use')

argparser.add_argument('-v', '--version',
    action='version',
    version='%(prog)s 1.0')

argparser.add_argument('-u', '--unit',
    choices=unit_values,
    required=False,
    action=SetUnitAction,
    dest='unit',
    default=Unit['FAHRENHEIT'],
    help=('Specify the unit that will be used to display '
    'the temperatures.'))

# Forecast option, technically required and will be validated
argparser.add_argument('-td', '--today',
    dest='forecast_option',
    action='store_const',
    const=ForecastType.TODAY,
    help='Show the weather forecast for the current day')

# argparser.add_argument('-5d', '--fivedays',
#                        dest='forecast_option',
#                        action='store_const',
#                        const=ForecastType.FIVEDAYS,
#                        help='Shows the weather forecast for the next 5 days')

# argparser.add_argument('-10d', '--tendays',
#                        dest='forecast_option',
#                        action='store_const',
#                        const=ForecastType.TENDAYS,
#                        help='Shows the weather forecast for the next 10 days')

# argparser.add_argument('-w', '--weekend',
#                        dest='forecast_option',
#                        action='store_const',
#                        const=ForecastType.WEEKEND,
#                        help=('Shows the weather forecast for the next or '
#                              'current weekend'))

# Validates the forecast option
def _validate_forecast_args(args):
    if args.forecast_option is None:
        err_msg = ('One of these arguments must be used: '
                   '-td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend')

        print(f'{argparser.prog}: error: {err_msg}', file=sys.stderr)
        sys.exit()

# Get args and validate
args = argparser.parse_args()
_validate_forecast_args(args)

# Choose parser and run
p = parsers[args.parser]
parser = p()
results = parser.run(args)

# Get results
print(f"[+] Weather Report for {args.city}")
print()
print(results)

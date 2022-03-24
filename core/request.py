import requests

class Request:
    '''
    Used for fetching API data
    '''
    def __init__(self, base_url):
        self._base_url = base_url

    def fetch_data(self, city):
        url = self._base_url.format(city=city)
        r = requests.get(url)

        if r.status_code == '404':
            error_message = ('Could not find the area that you '
                             'searching for')
            raise Exception(error_message)

        return r.content
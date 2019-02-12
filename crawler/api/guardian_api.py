import requests

api_key = '...'
api_url = 'http://content.guardianapis.com'


def request(url, from_date=None, to_date=None, page=1, page_size=50):
    parameters = {
        'api-key': api_key,
        'page': page,
        'page-size': page_size,
        'from-date': from_date,
        'to-date': to_date
    }
    return requests.get(url, params=parameters).json()['response']


def get_endpoint_url(endpoint):
    return f'{api_url}/{endpoint}'

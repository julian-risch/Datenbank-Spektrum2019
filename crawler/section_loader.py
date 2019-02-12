from crawler.api.guardian_api import request, get_endpoint_url


def parse_section(result):
    return {
        'name': result['id'],
        'title': result['webTitle'],
        'url': result['webUrl'],
        'apiUrl': result['apiUrl']
    }


def parse_section_results(results):
    return [parse_section(result) for result in results]


def get_sections():
    url = get_endpoint_url('sections')
    response = request(url)
    results = response['results']
    return parse_section_results(results)

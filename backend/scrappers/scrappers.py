import requests
from bs4 import BeautifulSoup

def get_jobs_num_linkedin(search_string, country):

    country_dict = {
        'co': 'Colombia',
        'pe': 'Peru',
        'ar': 'Argentina',
        'cr': 'Costa%20Rica',
        'ec': 'Ecuador',
        'br': 'Brazil',
        'mx': 'Mexico',
        'cl': 'Chile',
        'pa': 'Panama'
        }

    search_string = search_string.capitalize()

    important_items = ['Past 24 hours', 'Past Week ', 'Past Month ', 'Entry level', 'Associate', 'Mid-Senior', 'Director', 'Any Time']

    search_string = search_string.strip()

    URL = 'http://www.linkedin.com/jobs/search?keywords={}&location={}&redirect=false&position=1&pageNum=0'.format(search_string, country_dict[country])
    return parser_linkedin(URL, important_items)


def parser_linkedin(URL, important_items):
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    output = {}
    for item in important_items:
        output[item.strip().replace(' ', '_')] = 0

    results = soup.find_all('label', attrs={'class':'filter-list__list-item-label'})

    for result in results:
        result_text = result.text
        num_jobs, item = extract_filters_linkedin(result_text, important_items)
        if num_jobs != False and num_jobs != '':
            output[item.strip().replace(' ', '_')] = num_jobs
            
    return output

def extract_filters_linkedin(result_text, important_items):
    for item in important_items:
        if item in result_text:
            num_jobs = get_digits_from_str(result_text.replace(item, ''))
            return num_jobs, item
    
    return False, False

def get_jobs_num_computrabajo(search_string, country):
    search_string = search_string.strip()
    URL = 'https://www.computrabajo.com.{}/trabajo-de-{}?q={}'.format(country, search_string, search_string)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find('div', attrs={'class':'breadtitle_mvl'})
    result_span = result.find('span')
    if result_span == None:
        return {'Any_Time': '0'}
    else:
        return {'Any_Time': result_span.text}

def get_jobs_num_indeed(search_string, country):
    search_string = search_string.strip()
    URL = 'https://{}.indeed.com/Empleos-de-{}'.format(country, search_string)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find('div', attrs={'id':'searchCountPages'})
    num_jobs = result.text.replace('Página 1 de ', '').replace('empleos', '').replace('vagas', '').strip()
    return {'Any_Time': get_digits_from_str(num_jobs)}

def get_jobs_num_opcionempleo(search_string, country):
    search_string = search_string.strip()
    if country != 'ec':
        URL = 'https://www.opcionempleo.com.{}/buscar/empleos?s={}'.format(country, search_string)
    else:
        URL = 'https://www.opcionempleo.{}/buscar/empleos?s={}'.format(country, search_string)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find('header', attrs={'class':'row'})
    return {'Any_Time': get_digits_from_str(result.text)}

def get_digits_from_str(text):
    list_of_digits = [char for char in text if char.isdigit()]
    return ''.join(list_of_digits)


if __name__ == '__main__':
    # print(get_jobs_num_linkedin('Python', 'mx'))
    print(get_jobs_num_computrabajo('Python', 'pa'))
    # print(get_jobs_num_indeed('python', 'co'))
    # print(get_jobs_num_opcionempleo('python', 'ec'))

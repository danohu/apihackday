
from private import API_KEY
from calais import Calais
calais = Calais(API_KEY, submitter="python-calais demo")

def people_from_text(text):
    place_types = ('City', 'Continent', 'Country', 'ProvinceOrState')
    result = calais.analyze(text)
    places = []
    for item in result.entities:
        if item['_type'] in place_types:
            places.append(item)
    return places


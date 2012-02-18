
from private import KEY_CALAIS
from calais import Calais
calais = Calais(KEY_CALAIS, submitter="python-calais demo")

def places_from_text(text):
    place_types = ('City', 'Continent', 'Country', 'ProvinceOrState')
    result = calais.analyze(text)
    places = []
    for item in result.entities:
        if item['_type'] in place_types:
            places.append(item)
    return places


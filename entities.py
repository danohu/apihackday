
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

def placelocations(places):
    output = []
    for place in places:
        try:
            latitude =  place['resolutions'][0]['latitude']
            longitude =  place['resolutions'][0]['longitude']
        except KeyError:
            latitude = None
            longitude = None
        output.append({
            'name' : place['name'],
            'latitude' : latitude,
            'longitude' : longitude,
            })
    return output



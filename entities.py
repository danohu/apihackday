
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
    return [placelocation(place) for place in places]

def context(place):
    instance = place['instances'][0]
    return '%s <b>%s</b> %s' % (instance['prefix'], instance['exact'], instance['suffix'])

def placelocation(place):
    try:
        latitude =  place['resolutions'][0]['latitude']
        longitude =  place['resolutions'][0]['longitude']
    except KeyError:
        latitude = None
        longitude = None
    return {
        'name' : place['name'],
        'latitude' : latitude,
        'longitude' : longitude,
        'context' : context(place),
        }

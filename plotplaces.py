'''
For a given MP:
 download the text of their parliamentary statements from they work for you
 extract entities using opencalais
 plot them on a map
'''
import entities, parliament
import copy

def demo():
    text = parliament.mptext()
    places = entities.places_from_text(text)
    placenames = [x['name'] for x in places]
    print('places named by William Hague')
    print('\n'.join(placenames))

def raw_placeinfo(mpid = '10251'):
    mpcontext = {
            'mp' : parliament.mpinfo(mpid)
            }
    speeches = parliament.mpspeeches(mpid)['rows'][2:6]
    places = []
    for speech in speeches:
        speechcontext = copy.copy(mpcontext)
        speechcontext['speech'] = speech
        try:
            return entities.places_from_text(speech['body'])
            for place in newplaces:
                placecontext = copy.copy(speechcontext)
                placecontext.update(entities.placelocation(place))
                places.append(placecontext)
        except Exception:
            raise
            print('no entities')
        '''
        try:
            for place in entities.places_from_text(speech['body']):
                placecontext = copy.copy(speechcontext)
        except RuntimeError: #Exception:
            raise
            print('no entities')
        '''
    return places
    
 

if __name__ == '__main__':
    demo()

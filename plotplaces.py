'''
For a given MP:
 download the text of their parliamentary statements from they work for you
 extract entities using opencalais
 plot them on a map
'''
import entities, parliament

def demo():
    text = parliament.mptext()
    places = entities.places_from_text(text)
    placenames = [x['name'] for x in places]
    print('places named by William Hague')
    print('\n'.join(placenames))

if __name__ == '__main__':
    demo()

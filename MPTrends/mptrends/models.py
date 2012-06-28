from persistent.mapping import PersistentMapping
from twfy import TWFY
import json
import re
from kales import Kales


class MPTrends(PersistentMapping):

    def getGraphData(self,search,ids):
        data = {}
        for mpid in ids:
            freq = {}
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = theywork.api.getHansard(output = 'js', person = mpid, search = search)
            text = ''.join(x for x in rawtxt if ord(x)<127)
            speeches = json.loads(text)['rows']
            for row in speeches:
                #import ipdb; ipdb.set_trace()
                if(freq.get(row['hdate']) == None):
                    freq[row['hdate']] = 1
                else:
                    freq[row['hdate']] += 1
            data[mpid] = freq
            del freq
        return data

    def mptext(mpid = '10251'): #default is william hague
        jstxt = mpspeeches(mpid)
        statements = [x['body'] for x in jstxt['rows']]
        return '\n'.join(statements)
    
    def mpspeeches(self,mpid):
        theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
        rawtxt = theywork.api.getHansard(output = 'js', person = mpid)
        #import ipdb; ipdb.set_trace()
        text = ''.join(x for x in rawtxt if ord(x)<127)
        return json.loads(text)
    
    def mplist():
         mplist = theywork.api.getMPs(output = 'js')
         asciisafe = ''.join(x for x in mplist if ord(x) < 127)
         return json.loads(asciisafe)
    
    def places_for_text(speech, context):
        results = []
        places = entities.places_from_text(text)
        for place in places:
            thiscontext = copy.copy(context)
            thiscontext.update(entities.placelocation(place))
            results.append(thiscontext)
        return results
    
    def mpinfo(mpid):
        return theywork.api.getMP(output = 'js', id = mpid)
    
    def placeinfo(mpid = '10251'):
        mpcontext = {
                'mp' : mpinfo(mpid)
                }
        speeches = mpspeeches(mpid)
        for speech in speeches['rows']:
            speechcontext = copy.copy(mpcontext)
            speechcontext['speech'] = speech
            try:
                for place in entities.places_from_text(speech['body']):
                    placecontext = copy.copy(speechcontext)
                    placecontext.update(placelocation(place))
                    results.append(placecontext)
            except Exception:
                print('no text for %s' % speech['body'])
        return results
    
        speeches = js
    
        places = context_for_speech(places)
    
        __parent__ = __name__ = None

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MPTrends()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

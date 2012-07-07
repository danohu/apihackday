from persistent.mapping import PersistentMapping
from persistent import Persistent
from twfy import TWFY
from time import time
import json
import re
from kales import Kales


class MPTrends(PersistentMapping):
    __parent__ = __name__ = None

    def chart(self,search,mpids):
        data = []
        for mpid in mpids:
            # TODO: check for cached version of this query, 24 hr expiry
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = str(theywork.api.getHansard(output = 'js', person = mpid, search = search))
            text = ''.join(x for x in rawtxt if ord(x)<127)
            speeches = json.loads(text)['rows']
            data.append({'mpid':mpid,'speeches':speeches})
         
        # This is for Google Charts data structure

        firstrow = ['Date']
        dates = []
        for MP in data:
            firstrow.append(MP['mpid'])
            for speech in MP['speeches']:
                dates.append(speech['hdate'][:-3])
        
        dates = sorted(list(set(dates)))

        rows = []
        for date in dates:
            rows.append([date])

        me = 1
        for MP in data:
            for row in rows:
                row.append(0)
            for speech in MP['speeches']:
                for row in rows:
                    if row[0] == speech['hdate'][:-3]:
                        row[me] = row[me] + 1
            me = me + 1
        rows.insert(0,firstrow)
        return rows

    def mplist(self):
        theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
        rawtxt = str(theywork.api.getMPs(output = 'js'))
        text = ''.join(x for x in rawtxt if ord(x)<127)
        MPs = json.loads(text)
        self['cache']['mplist'] = {'json':MPs,'time':time()}
        import ipdb; ipdb.set_trace()
        if expiry > (time()+5184000):
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = str(theywork.api.getMPs(output = 'js'))
            text = ''.join(x for x in rawtxt if ord(x)<127)
            MPs = json.loads(text)
            self['cache']['mplist'] = {'json':MPs,'time':time()}
            print 'cache missed'
            return MPs
        else:
            print 'cache hit'
            return self['cache']['mplist']['time']

class Cache(Persistent):
     def mplist(self):
        import ipdb; ipdb.set_trace()
        theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
        rawtxt = str(theywork.api.getMPs(output = 'js'))
        text = ''.join(x for x in rawtxt if ord(x)<127)
        MPs = json.loads(text)
        self['cache']['mplist'] = {'json':MPs,'time':time()}
        import ipdb; ipdb.set_trace()
        if expiry > (time()+5184000):
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = str(theywork.api.getMPs(output = 'js'))
            text = ''.join(x for x in rawtxt if ord(x)<127)
            MPs = json.loads(text)
            self['cache']['mplist'] = {'json':MPs,'time':time()}
            print 'cache missed'
            return MPs
        else:
            print 'cache hit'
            return self['cache']['mplist']['time']

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MPTrends()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

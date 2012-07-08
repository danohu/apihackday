from persistent.mapping import PersistentMapping
from persistent import Persistent
from twfy import TWFY
import json
import re
from time import time
from crypt import crypt
from collections import defaultdict
from kales import Kales


class MPTrends(PersistentMapping):
    __parent__ = __name__ = None

    def chart(self,search,mpids):
        data = []
        for mpid in mpids:
            searchHash = crypt(''.join([search,mpid]),'ok')
            if self['cache'].get(searchHash) == None or self['cache'][searchHash]['time'] < time()-5184000:
                print 'chart cache missed :('
                theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
                rawtxt = str(theywork.api.getHansard(output = 'js', person = mpid, search = search, num = 1000))
                text = ''.join(x for x in rawtxt if ord(x)<127)
                speeches = json.loads(text)['rows']
                self['cache'][searchHash] = {
                    'speeches':speeches,
                    'time':time(),
                }
                data.append({
                    'mpid':mpid,
                    'speeches':speeches,
                })
            else:
                print 'chart cache hit :)'
                data.append({'mpid':mpid,'speeches':self['cache'][searchHash]['speeches']})
         
        # This is for Google Charts data structure

        firstrow = ['Date']
        dates = []
        for MP in data:
            speaker = MP['speeches'][0]['speaker']
            firstrow.append(speaker['first_name']+' '+speaker['last_name'])
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
        if self.get('cache') == None: self['cache'] = {}
        if self['cache'].get('mplist') == None or self['cache']['mplist']['time'] < time()-5184000:
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = str(theywork.api.getMPs(output = 'js'))
            text = ''.join(x for x in rawtxt if ord(x)<127)
            MPs = json.loads(text)
            MPs.sort(key=lambda MP: MP['name'].split(' ')[1])
            parties = {}
            for MP in MPs:
                if parties.get(MP['party']) == None:
                    parties[MP['party']] = []
                    parties[MP['party']].append(MP)
                else:
                    parties[MP['party']].append(MP)
            self['cache']['mplist'] = {
                'data':parties,
                'time':time(),
            }
            print 'mplist cache missed :('
            return parties
        else:
            print 'mplist cache hit :)'
            return self['cache']['mplist']['data']

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MPTrends()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

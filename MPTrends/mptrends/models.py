from persistent.mapping import PersistentMapping
from persistent import Persistent
from twfy import TWFY
import json
import re
from kales import Kales


class MPTrends(PersistentMapping):
    __parent__ = __name__ = None

    def graph(self,search,mpids):
        data = []
        for mpid in mpids:
            # TODO: check for cached version of this query, 24 hr expiry
            theywork = TWFY.TWFY('AqHCxnC7THtNEPXRyBAcHUfU')
            rawtxt = str(theywork.api.getHansard(output = 'js', person = mpid, search = search))
            text = ''.join(x for x in rawtxt if ord(x)<127)
            speeches = json.loads(text)['rows']
            data.append({'mpid':mpid,'speeches':speeches})
         
        # This is for Google Charts data structure
        dates = []
        for MP in data:
            for speech in MP['speeches']:
                dates.append(speech['hdate'])
        
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
                    if row[0] == speech['hdate']:
                        row[me] = row[me] + 1
            me = me + 1

        return rows


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MPTrends()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

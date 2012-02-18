from private import KEY_TWFY
from twfy import TWFY
import json

theywork = TWFY.TWFY(KEY_TWFY)

def mptext(mpid = '10251'): #default is william hague
    rawtxt = theywork.api.getHansard(output = 'js', person = mpid)
    jstxt = json.loads(rawtxt)
    statements = [x['body'] for x in jstxt['rows']]
    return '\n'.join(statements)


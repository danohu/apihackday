import os
import tornado.ioloop
import tornado.web
import json
import entities, parliament
import urllib2

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=1)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        indextxt = open('./site/index.html').read()
        self.write(indextxt)

class DemoHandler(tornado.web.RequestHandler):

    def mp_places(self, mpid):
        mckey = str('places_%s' % mpid)
        places = mc.get(mckey)
        if places is None:
            text = parliament.mptext()
            places = entities.places_from_text(text)
            mc.set(mckey, places)
        return places

    def get_locations(self, mpid):
        places = self.mp_places(mpid)
        locations = entities.placelocations(places)
        return json.dumps(locations)
        
    def get(self):
        mpid = self.get_argument('mp', '10251')
        self.content_type = 'application/json'
        self.set_header("Content-Type", "application/json") 
        self.write(self.get_locations(mpid))


class NewDemoHandler(tornado.web.RequestHandler):
    def get(self):
        mpid = self.get_argument('mp', '10251')
        mckey = str('places_%s' % mpid)
        places = mc.get(mckey)
        if places is None:
            text = parliament.mptext()
            places = entities.places_from_text(text)
            mc.set(mckey, places)
        locations = entities.placelocations(places)
        output = json.dumps(locations)
        self.content_type = 'application/json'
        self.set_header("Content-Type", "application/json") 
        self.write(output)

class MPListHandler(tornado.web.RequestHandler):
    def get(self):
        cached = mc.get('mplist')
        if cached is None:
            mplist = urllib2.urlopen('http://www.theyworkforyou.com/api/getMPs?key=C96JqqCACkSJGaXNMyGxyLei&output=js').read()
            mc.set('mplist', mplist)
        self.set_header("Content-Type", "application/json") 
        self.write(cached or mplist)


static_path =  os.path.join(os.path.dirname(__file__), "static")

application = tornado.web.Application([ 
    (r"/", MainHandler),
    (r"/code/demo", DemoHandler),
    (r"/code/mplist", MPListHandler),
                            ])
if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

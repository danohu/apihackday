
import tornado.ioloop
import tornado.web
import json
import entities, parliament

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=1)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        mpid = '10251'
        mckey = 'places_%s' % mpid
        places = mc.get(mckey)
        if places is None:
            text = parliament.mptext()
            places = entities.places_from_text(text)
            mc.set(mckey, places)
        locations = entities.placelocations(places)
        output = json.dumps(locations)
        self.write(output)
        #placenames = [x['name'] for x in places]

 
application = tornado.web.Application([ 
    (r"/", MainHandler),
    (r"/demo", DemoHandler),

                            ])
if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

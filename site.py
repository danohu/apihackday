
import tornado.ioloop
import tornado.web
import json
import entities, parliament

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        text = parliament.mptext()
        places = entities.places_from_text(text)
        output = json.dumps(places)
        self.write(output)
        #placenames = [x['name'] for x in places]

 
application = tornado.web.Application([ 
    (r"/", MainHandler),
    (r"/demo", DemoHandler),

                            ])
if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

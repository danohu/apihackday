# MPTrends: showing which places MPs talk about

Which places do MPs talk about?

This service analyzes the text of an MPs parliamentary contributions, extracting places they mention by name. It presents these on a map interface, one point per mention.

We use TheyWorkForYou to provide structured text from parliament, OpenCalais to identify placenames from that text, and Google Maps to display them.

One-day hack project from February 2012 API Hackathon (http://apihackathonlondon.eventbrite.com/)

It is currently running at http://viz.ohuiginn.net/

# Install

1) Get API Keys

2 API keys are required, in a file private.py. This is not in github to prevent misuse. You will need to get keys from:

- http://www.opencalais.com/APIkey
- http://www.theyworkforyou.com/api/key

Create the file private.py containing the keys:
KEY_CALAIS = 'XXX'
KEY_TWFY = 'XXX'

2) Install python libraries

Libraries for opencalais and theyworkforyou are included in this repo
Tornado and memcached libraries are also required, and can be installed with:

$ pip install tornado python-memcached

3) install memcached

We expect memcached to be running on port 11211. You can arrange this on debian/ubuntu with:

#apt-get install memcached

4) Set up web server

To run the web service, you will need a webserver pointing urls in /code at the tornado process (on port 9000), and everything else at the static content in /site

An config file for nginx is included. Copy this into /etc/nginx/sites-enabled, and reload nginx ("/etc/init.d/nginx reload"). You'll probably need to modify it for your own domain etc.

5) start it up

$ python site.py

#Credits

@danohu
@bmcorser
@roppa_uk
@surinder

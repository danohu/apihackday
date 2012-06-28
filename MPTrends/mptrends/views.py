from pyramid.view import view_config
from pyramid.response import Response
from .models import MPTrends
import re

@view_config(context=MPTrends, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='json', route_name='graph_json')
def graph_json(request):
    for mpid in request.matchdict['ids']:
        speeches = request.context.mpspeeches(int(mpid))['rows']
        #import ipdb; ipdb.set_trace()
        for row in speeches:
            print re.search(request.matchdict['search'],row['body'])
    return request.context.mpspeeches(int(request.matchdict['ids'][0]))

@view_config(context=MPTrends, renderer='json', route_name='map_json')
def map_json(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='templates/graph.pt', route_name='graph')
def graph(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='templates/map.pt', route_name='map')
def map(request):
    return {'project':'MPTrends'}

from pyramid.view import view_config
from pyramid.response import Response
from .models import MPTrends
import re

@view_config(context=MPTrends, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='json', route_name='chart_json')
def chart_json(request):
    r = request.matchdict
    graphData = request.context.chart(r['search'],r['ids'])
    return graphData

@view_config(context=MPTrends, renderer='json', route_name='map_json')
def map_json(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='templates/graph.pt', route_name='graph')
def graph(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='templates/map.pt', route_name='map')
def map(request):
    return {'project':'MPTrends'}

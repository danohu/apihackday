from pyramid.view import view_config
from .models import Graph, Map, MyModel

@view_config(context=MyModel, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=Graph, renderer='json', route_name='graph_json')
def graph_json(request):
    return request

@view_config(context=Map, renderer='json', route_name='map_json')
def graph_json(request):
    return {'project':'MPTrends'}


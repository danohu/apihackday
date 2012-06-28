from pyramid.view import view_config
from .models import MPTrends

@view_config(context=MPTrends, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='json', route_name='graph_json')
def graph_json(request):
    return request

@view_config(context=MPTrends, renderer='json', route_name='map_json')
def map_json(request):
    return {'project':'MPTrends'}


from pyramid.view import view_config
from pyramid.response import Response
from .models import MPTrends

@view_config(context=MPTrends, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=MPTrends, renderer='json', route_name='graph_json')
def graph_json(request):
    something = [1,2,3,4]
    import ipdb; ipdb.set_trace()
    return something

@view_config(context=MPTrends, renderer='json', route_name='map_json')
def map_json(request):
    return {'project':'MPTrends'}


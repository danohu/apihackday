from pyramid.view import view_config
from .models import MyModel

@view_config(context=MyModel, renderer='templates/home.pt', route_name='home')
def home(request):
    return {'project':'MPTrends'}

@view_config(context=MyModel, renderer='templates/json/speaker.pt', route_name='speaker_json_route')
def speaker_json_view(request):
    return {'project':'MPTrends'}

@view_config(context=MyModel, renderer='templates/speaker.pt', route_name='speaker_route')
def speaker_view(request):
    return {'project':'MPTrends'}

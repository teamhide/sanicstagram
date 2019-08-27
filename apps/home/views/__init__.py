from sanic import Blueprint

from apps.home.views.home_view import Home

bp = Blueprint('home')
bp.add_route(Home.as_view(), '')

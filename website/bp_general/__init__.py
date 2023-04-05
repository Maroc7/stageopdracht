from flask import Blueprint

bp_general = Blueprint('bp_general', __name__, cli_group=None)

from .views_general import views_gn
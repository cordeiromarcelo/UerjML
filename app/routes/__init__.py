import typing as t

from flask import Blueprint
from jinja2 import Environment
from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

platform = Blueprint('platform', __name__, url_prefix='/')

@platform.app_template_filter('new_tojson')
def new_tojson_filter(value: t.Any) -> Markup:
    env = Environment()
    dumps = env.policies["json.dumps_function"]
    kwargs = {'sort_keys': False}
    return htmlsafe_json_dumps(value, dumps=dumps, **kwargs)
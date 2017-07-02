from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

web_gui = Blueprint('web_gui', __name__, url_prefix='/gui', template_folder='templates')

@web_gui.route('/', defaults={'page': 'select'})
@web_gui.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)

from flask import Blueprint, render_template, request

bp = Blueprint('search', __name__)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    # En XSS Reflected, el backend recibe el dato y lo devuelve al template.
    # La vulnerabilidad real se gestiona en search.html (usando |safe o no).
    return render_template('search.html', query=query)
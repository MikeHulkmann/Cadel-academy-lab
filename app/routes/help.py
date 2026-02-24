from flask import Blueprint, render_template, request, redirect
from utils.middleware import get_security_level
from urllib.parse import urlparse

bp = Blueprint('help', __name__)

@bp.route('/help')
def index():
    return render_template('help.html')

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@bp.route('/redirect')
def external_redirect():
    target_url = request.args.get('target')
    if not target_url:
        return "No se especificó un destino.", 400

    if get_security_level() == 'vulnerable':
        # [VULNERABLE] Open Redirect: Redirige a cualquier URL sin validación.
        # Payload: /redirect?target=https://youtube.com
        return redirect(target_url)
    else:
        # [SEGURO] Validación de URL
        # Solo permite redirecciones a la misma aplicación o relativas.
        parsed_url = urlparse(target_url)
        if parsed_url.netloc == '' or parsed_url.netloc == request.host:
             return redirect(target_url)
        else:
             return "Redirección externa no permitida.", 400
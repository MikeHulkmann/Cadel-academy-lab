from flask import Blueprint, render_template

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
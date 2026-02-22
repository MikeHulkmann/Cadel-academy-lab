from flask import Blueprint, render_template

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def dashboard():
    # La validación de cookies se hace en el frontend (JS) y en el navegador
    return render_template('dashboard.html')
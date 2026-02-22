from flask import request, g, current_app

def load_security_level():
    """
    Middleware para establecer el nivel de seguridad basado en la cookie.
    
    Este mecanismo permite cambiar entre modo 'vulnerable' y 'secure' en tiempo real
    sin necesidad de reiniciar el contenedor, simplemente cambiando una cookie en el navegador.
    """
    security_level = request.cookies.get('security_level')

    # Si la cookie no existe (primera visita), usa el valor por defecto definido en docker-compose
    if not security_level:
        security_level = current_app.config.get('SECURITY_LEVEL', 'vulnerable')

    # Guardamos el nivel en 'g' (global request context) para acceder desde cualquier parte de la petición
    g.security_level = security_level

def get_security_level():
    """Retorna el nivel de seguridad actual para la petición en curso."""
    return g.security_level

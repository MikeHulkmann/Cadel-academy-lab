# Auditoría: Reconocimiento y Divulgación de Información

## Descripción
La fase de reconocimiento es crucial en cualquier auditoría. A menudo, los desarrolladores dejan archivos de configuración, copias de seguridad o instrucciones para robots (`robots.txt`) que revelan la estructura oculta del sitio o credenciales sensibles.

## 🕵️ Reproducción

1.  **Análisis de `robots.txt`:**
    *   Navega a `http://localhost:8080/robots.txt`.
    *   Observa que existe una entrada `Disallow: /secret_config`. Esto indica que esa ruta existe pero el administrador no quiere que sea indexada por buscadores.

2.  **Acceso a Rutas Ocultas:**
    *   Navega a `http://localhost:8080/secret_config`.
    *   **Resultado:** El servidor devuelve credenciales de base de datos y claves API en texto plano.

## 🔍 Análisis del Código

**Código Vulnerable (`app/app.py`):**
```python
@app.route('/robots.txt')
def robots():
    # Revela la existencia de /secret_config
    content = "User-agent: *\nDisallow: /secret_config\n"
    return Response(content, mimetype='text/plain')

@app.route('/secret_config')
def secret_config():
    # Expone información sensible sin autenticación
    content = "DB_HOST=localhost\nDB_USER=root\nDB_PASS=root\nAPI_KEY=12345-ABCDE"
    return Response(content, mimetype='text/plain')
```

## 🛡️ Solución

1.  **No exponer rutas sensibles en `robots.txt`:** La seguridad por oscuridad no funciona. Si una ruta es privada, debe estar protegida por autenticación, no solo oculta.
2.  **Proteger archivos de configuración:** Asegurarse de que el servidor web no sirva archivos `.env`, `.git`, o rutas de configuración interna.
3.  **Autenticación:** Requerir sesión activa (`if 'user_id' not in session`) para acceder a cualquier ruta que contenga datos del sistema.
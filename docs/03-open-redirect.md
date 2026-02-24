# Auditoría: Open Redirect (Redirección Abierta)

## Descripción
Una vulnerabilidad de Redirección Abierta (Open Redirect) ocurre cuando una aplicación web redirige a un usuario a una URL externa especificada en un parámetro de la petición, sin validar que el destino sea seguro o esté dentro de una lista blanca.

Los atacantes abusan de esta confianza para redirigir a las víctimas a sitios de phishing o de descarga de malware, utilizando el dominio legítimo de la aplicación como un disfraz para hacer que el enlace parezca seguro.

## 🕵️ Vectores de Ataque

### 1. Redirección Clásica (Parámetro GET)
Este es el vector más común. La aplicación tiene una funcionalidad de redirección, a menudo usada después de un login o para dirigir a páginas de salida.

*   **URL Vulnerable:** `https://app-segura.com/redirect?url=http://sitio-malicioso.com`
*   **Impacto:** Phishing, distribución de malware. El usuario confía en `app-segura.com`, pero es redirigido a un sitio peligroso.

### 2. Redirección vía XSS Stored
Aunque técnicamente es una explotación de XSS, el resultado final es una redirección. El atacante inyecta un script persistente que modifica el `window.location` del navegador.

*   **Payload:** `<script>window.location='http://sitio-malicioso.com'</script>`
*   **Impacto:** Similar al anterior, pero más potente, ya que no requiere que la víctima haga clic en un enlace manipulado. Cualquier visitante de la página infectada es redirigido.

## 🛠️ Herramientas de Auditoría

*   **Burp Suite / ZAP:** Para interceptar peticiones y modificar parámetros de URL en busca de puntos de redirección.
*   **Navegador Web:** Las herramientas de desarrollador (F12) son suficientes para observar las cabeceras `Location` en las respuestas de redirección (código 302 o 301).

## 🔍 Análisis del Código Vulnerable

**Ejemplo en `app/routes/help.py` (Modo Vulnerable):**

```python
@bp.route('/redirect')
def external_redirect():
    target_url = request.args.get('target')
    if target_url:
        # [VULNERABLE] No hay validación sobre target_url
        return redirect(target_url)
```
El código toma el parámetro `target` y lo usa directamente en una función de redirección, confiando ciegamente en la entrada del usuario.

## 🛡️ Solución (Versión Segura)

La mitigación consiste en validar la URL de destino contra una **lista blanca (whitelist)** de dominios permitidos o, como mínimo, asegurar que la redirección sea a una página dentro del mismo dominio.

**Enfoque 1: Lista Blanca Estricta**
```python
ALLOWED_DOMAINS = ['cadel.academy', 'docs.cadel.academy']
parsed_url = urlparse(target_url)
if parsed_url.netloc in ALLOWED_DOMAINS:
    return redirect(target_url)
else:
    return "Redirección no permitida."
```

**Enfoque 2: Misma Aplicación (Implementado en Cadel Academy)**
```python
# [SEGURO] Solo permite redirecciones relativas o al mismo host.
parsed_url = urlparse(target_url)
if parsed_url.netloc == '' or parsed_url.netloc == request.host:
     return redirect(target_url)
else:
     return "Redirección externa no permitida."
```
Este enfoque es más seguro y simple. Si `netloc` está vacío, es una ruta relativa (ej. `/dashboard`). Si `netloc` coincide con el host de la petición, es una ruta absoluta dentro de la misma aplicación. Cualquier otro caso es bloqueado.
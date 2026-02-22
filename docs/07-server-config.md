# Auditoría: Configuración del Servidor

## Descripción
Una configuración robusta del servidor web es la primera línea de defensa. La falta de HTTPS y de cabeceras de seguridad HTTP expone a los usuarios a ataques de interceptación (MitM), Clickjacking y otros vectores.

## 🕵️ Análisis de Cabeceras

Puedes usar las herramientas de desarrollador (F12 -> Red) o `curl -I` para inspeccionar las cabeceras de respuesta.

### Versión Vulnerable (Puerto 8080)
*   **Protocolo:** HTTP (Texto plano).
*   **Cabeceras Faltantes:**
    *   `Strict-Transport-Security` (HSTS)
    *   `X-Frame-Options`
    *   `X-Content-Type-Options`
    *   `Content-Security-Policy` (CSP)

### Versión Segura (Puerto 8443)
*   **Protocolo:** HTTPS (TLS 1.2/1.3).
*   **Cabeceras Presentes:**
    *   `Strict-Transport-Security`: Fuerza al navegador a usar siempre HTTPS.
    *   `X-Frame-Options: SAMEORIGIN`: Previene ataques de Clickjacking (no se puede embeber en iframes de otros dominios).
    *   `X-XSS-Protection: 1; mode=block`: Activa el filtro XSS nativo de navegadores antiguos.

## 🛡️ Configuración en Nginx

El archivo `docker/nginx/default.conf` implementa estas mejoras:

```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```
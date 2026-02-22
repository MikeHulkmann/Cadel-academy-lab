# Laboratorio 07: Reconocimiento y Archivos Ocultos

## 🎯 Objetivo
Utilizar técnicas de reconocimiento básico para descubrir archivos y rutas ocultas que revelen información sensible del servidor.

## 📋 Prerrequisitos
1.  Modo Vulnerable activo.
2.  Opcional: Herramienta `nmap` o `curl`.

## 📝 Instrucciones Paso a Paso

### Paso 1: Inspección de robots.txt
1.  Los administradores suelen usar `robots.txt` para ocultar rutas a Google, pero esto también le dice a los hackers dónde mirar.
2.  Navega a: `http://localhost:8080/robots.txt`.
3.  Lee el contenido. Deberías ver una línea `Disallow: /secret_config`.

### Paso 2: Acceso al recurso oculto
1.  Intenta navegar a la ruta descubierta: `http://localhost:8080/secret_config`.
2.  Observa el contenido devuelto.

### Paso 3: Escaneo automatizado (Opcional)
1.  Si tienes `nmap` instalado, abre una terminal.
2.  Ejecuta:
    ```bash
    nmap -p 8080 --script http-enum localhost
    ```
3.  Observa si Nmap descubre automáticamente estas rutas.

## 🏁 Verificación
*   Debes haber encontrado credenciales o información de configuración en la ruta `/secret_config`.

## 🛡️ Preguntas de Reflexión
1.  ¿Es `robots.txt` un mecanismo de seguridad válido?
2.  ¿Qué es la "Seguridad por Oscuridad" y por qué falla?

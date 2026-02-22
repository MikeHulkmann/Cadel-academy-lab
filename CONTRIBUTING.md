# Contribuir a Cadel Academy

¡Gracias por tu interés en mejorar este entorno de entrenamiento!

## Cómo añadir nuevas vulnerabilidades

1.  **Crea una nueva ruta:** Añade la lógica en `app/routes/`. Asegúrate de usar el middleware `get_security_level()` para implementar tanto la versión vulnerable como la segura.
2.  **Crea la vista:** Añade la plantilla HTML en `app/templates/`.
3.  **Documenta:** Crea un archivo `.md` en `docs/` explicando la vulnerabilidad, cómo reproducirla y cómo solucionarla.
4.  **Registra:** No olvides registrar el Blueprint en `app/app.py`.

## Estilo de Código

*   **Python:** Seguimos PEP 8.
*   **HTML/CSS:** Usamos Bootstrap 5. Mantén el soporte para Dark Mode usando las variables CSS definidas en `style.css`.

## Pull Requests

Por favor, asegúrate de que tu código pasa las pruebas manuales (funciona el interruptor de seguridad) antes de enviar un PR.
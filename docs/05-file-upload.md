# Auditoría: Subida de Archivos Sin Restricciones (Unrestricted File Upload)

## Descripción
La funcionalidad de subida de archivos es común en aplicaciones web, pero si no se implementa correctamente, puede ser devastadora. Permitir que los usuarios suban archivos sin validar estrictamente su tipo, extensión y contenido puede llevar a:
*   **Remote Code Execution (RCE):** Subida de scripts de servidor (PHP, JSP, PY) que el atacante puede ejecutar.
*   **XSS Stored:** Subida de archivos HTML o SVG con scripts maliciosos.
*   **Defacement:** Sobrescritura de archivos críticos del sistema.

## 🕵️ Reproducción

1.  Navega a `http://localhost:8080/forum` (Modo Vulnerable).
2.  En el formulario de "Crear Nueva Publicación", selecciona la opción de subir archivo.
3.  **Prueba de XSS:** Crea un archivo `exploit.html` con:
    ```html
    <script>alert('XSS via File Upload')</script>
    ```
4.  Sube el archivo y publícalo.
5.  Haz clic en el enlace del archivo adjunto en el tablón. El script se ejecutará.

**Resultado:** El servidor acepta cualquier extensión. En un entorno real con un servidor web mal configurado (ej. Apache/PHP), podrías subir una *web shell* (`shell.php`) y tomar control total del servidor.

## 🔍 Análisis del Código

**Código Vulnerable (`app/routes/forum.py`):**
```python
# Se confía ciegamente en el nombre de archivo proporcionado por el usuario
filename = file.filename 
filepath = os.path.join(upload_folder, filename)
file.save(filepath) # Se guarda sin validación
```

## 🛡️ Solución (Versión Segura)

1.  Validar la extensión contra una lista blanca (`.pdf`, `.jpg`, etc.).
2.  Sanitizar el nombre del archivo usando `secure_filename` para evitar "Path Traversal" (ej. `../../etc/passwd`).

```python
if allowed_file(filename):
    filename = secure_filename(filename)
```
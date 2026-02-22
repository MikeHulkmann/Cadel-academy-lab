# Laboratorio 02: SQL Injection (Extracción de Datos)

## 🎯 Objetivo
Extraer información sensible de la base de datos (versión, usuarios) utilizando una vulnerabilidad de SQL Injection basada en UNION en el buscador del chat.

## 📋 Prerrequisitos
1.  Tener una sesión activa (puedes usar el Lab 01 para entrar como admin o registrar un usuario nuevo).
2.  Modo Vulnerable activo.

## 📝 Instrucciones Paso a Paso

### Paso 1: Localizar la Vulnerabilidad
1.  Ve a la sección de **Chat** (`/chat`).
2.  Localiza el formulario "Buscar Alumno".
3.  Introduce una comilla simple `'` y busca. Observa si hay errores.

### Paso 2: Determinar el número de columnas
1.  Para usar `UNION`, necesitamos saber cuántas columnas devuelve la consulta original.
2.  Prueba inyectando `ORDER BY`:
    *   `' ORDER BY 1 -- -` (Si no da error, hay al menos 1 columna)
    *   `' ORDER BY 5 -- -` (Si da error, hay menos de 5)
    *   Encuentra el número exacto donde deja de dar error. (Pista: Son 2 columnas: id y username).

### Paso 3: Inyección UNION
1.  Una vez confirmado el número de columnas (2), inyecta una consulta para unir resultados.
2.  Prueba:
    ```sql
    ' UNION SELECT 1, @@version -- -
    ```
3.  Observa los resultados de la búsqueda. Deberías ver la versión de MySQL en lugar de un nombre de usuario.

### Paso 4: Extracción de Datos
1.  Intenta extraer los nombres de usuario y contraseñas de la tabla `users`.
2.  Payload:
    ```sql
    ' UNION SELECT username, password FROM users -- -
    ```

## 🏁 Verificación
*   En la lista de resultados de búsqueda, deberías ver una lista de usuarios junto con sus contraseñas (o hashes).

## 🛡️ Preguntas de Reflexión
1.  ¿Por qué es necesario que el número de columnas coincida en una inyección UNION?
2.  ¿Cómo podrías automatizar este proceso usando SQLMap?

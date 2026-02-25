# Laboratorio 04c: SQL Injection (Escalada de Privilegios en Perfil)

## 🎯 Objetivo
Explotar una vulnerabilidad de Inyección SQL en el formulario de actualización de perfil para escalar privilegios a 'admin' o modificar los datos de otro usuario (IDOR).

## 📋 Prerrequisitos
1.  Tener una sesión activa (ej. como 'alumno').
2.  Modo Vulnerable activo.

## 📝 Instrucciones Paso a Paso

La vulnerabilidad reside en cómo la aplicación construye la consulta `UPDATE` al guardar los cambios del perfil, usando una concatenación directa en una sola línea. Esto nos permite "secuestrar" la consulta.

---

### Escenario A: Escalada de Privilegios (Convertirse en Admin)

**Objetivo:** Modificar nuestro propio rol de 'user' a 'admin'.

1.  **Navegación:** Ve a la sección **Mi Perfil**.
2.  **Inyección:** En el formulario de "Información Personal", localiza el campo **Bio**.
3.  **Payload:** Introduce el siguiente payload en el campo **Bio**:
    ```sql
    Estudiante ejemplar', role='admin' #
    ```
4.  **Ejecución:** Haz clic en "Guardar Cambios".

#### Análisis Técnico
La consulta SQL resultante en el servidor será:
```sql
UPDATE users SET ..., bio='Estudiante ejemplar', role='admin' #' WHERE id=3
```
*   `bio='Estudiante ejemplar'` cierra el campo bio.
*   `, role='admin'` añade una nueva asignación al `SET`, cambiando el rol.
*   `#` comenta el resto de la consulta, incluyendo la comilla de cierre original y la cláusula `WHERE`.
*   **Importante:** Como el `#` anula el `WHERE`, ¡este payload actualizará **TODOS** los usuarios a 'admin'! Esto es un efecto secundario peligroso y educativo.

#### Verificación
*   Refresca la página. En la tarjeta de perfil de la izquierda, tu rol ahora debería ser **admin**.

---

### Escenario B: Modificación de Datos de Otro Usuario (IDOR)

**Objetivo:** Cambiar el nombre completo del usuario 'admin' (cuyo ID es 1).

1.  **Navegación:** Ve a **Mi Perfil**.
2.  **Preparación:** En el campo **Nombre Completo**, escribe el nuevo nombre que quieres para el admin, por ejemplo: `Admin Pwned`.
3.  **Inyección:** En el campo **Bio**, introduce el siguiente payload:
    ```sql
    Bio sin importancia' WHERE id=1 #
    ```
4.  **Ejecución:** Haz clic en "Guardar Cambios".

#### Análisis Técnico
La consulta SQL resultante será:
```sql
UPDATE users SET full_name='Admin Pwned', ..., bio='Bio sin importancia' WHERE id=1 #' WHERE id=3
```
*   `bio='...'` cierra el campo bio.
*   `WHERE id=1` reemplaza la cláusula `WHERE` original, apuntando al usuario 'admin'.
*   `#` comenta el `WHERE id=3` original, evitando un error de sintaxis.

#### Verificación
*   Cierra sesión y ve al **Blog** o al **Foro**.
*   Busca una publicación del administrador. Su nombre de usuario ahora debería ser "Admin Pwned".

## 🛡️ Preguntas de Reflexión
1.  ¿Por qué es crucial que la consulta SQL en el código fuente esté en una sola línea para que estos ataques funcionen con `#`?
2.  En el Escenario A, ¿cómo modificarías el payload para que solo tu usuario sea promovido a 'admin' sin afectar a los demás? (Pista: No uses `#`).
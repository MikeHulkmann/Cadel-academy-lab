# Auditoría: SQL Injection en Login

## Descripción
La inyección SQL (SQLi) es una vulnerabilidad crítica que ocurre cuando los datos proporcionados por el usuario se concatenan directamente en una consulta a la base de datos sin validación ni escape. Esto permite a un atacante manipular la estructura de la consulta para acceder, modificar o eliminar datos no autorizados.

## 🕵️ Vectores de Ataque y Reproducción

### Caso 1: Bypass de Autenticación (Login)

1.  Navega a `http://localhost:8080/login` (Asegúrate de estar en modo vulnerable).
2.  En el campo **Usuario**, introduce el siguiente payload para saltarte la verificación de contraseña:
    ```sql
    admin' OR '1'='1' -- -
    ```
3.  En el campo **Contraseña**, escribe cualquier valor aleatorio.
4.  Pulsa "Entrar".

**Resultado:** Accederás al panel de control como el primer usuario de la base de datos (generalmente el administrador).

### Caso 2: Extracción de Datos (Buscador de Chat)

1.  Inicia sesión y ve a `http://localhost:8080/chat`.
2.  En el buscador de usuarios ("Buscar Alumno"), introduce una comilla simple `'`.
3.  Si la aplicación devuelve un error de base de datos o un comportamiento anómalo, es vulnerable.
4.  Intenta inyectar una consulta `UNION` para extraer datos de otras tablas (ej. contraseñas).

## 🔍 Análisis del Código

**Código Vulnerable (`app/routes/login.py`):**
```python
# Concatenación directa de strings. ¡Peligro!
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```
El uso de f-strings permite cerrar la comilla del string SQL (`'`) e inyectar lógica booleana (`OR '1'='1`), haciendo que la condición `WHERE` sea siempre verdadera.

## 🛡️ Solución (Versión Segura)

En la versión segura (`https://localhost:8443/login`), utilizamos **Consultas Parametrizadas**.

```python
query = "SELECT * FROM users WHERE username = %s AND password = %s"
cursor.execute(query, (username, password))
```

El motor de base de datos trata los inputs como datos literales, nunca como código ejecutable, neutralizando el ataque.

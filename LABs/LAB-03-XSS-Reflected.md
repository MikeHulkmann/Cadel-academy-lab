# Laboratorio 03: Cross-Site Scripting (Reflected)

## 🎯 Objetivo
Ejecutar código JavaScript arbitrario en el navegador reflejándolo a través del motor de búsqueda de la aplicación.

## 📋 Prerrequisitos
1.  Modo Vulnerable activo.

## 📝 Instrucciones Paso a Paso

### Paso 1: Identificar el punto de entrada
1.  Ve a la página de **Inicio** o usa la barra de navegación para ir a **Buscar**.
2.  Busca una palabra normal, por ejemplo "hola".
3.  Observa que la palabra "hola" se refleja en la página de resultados: "Resultados para: hola".

### Paso 2: Prueba de inyección HTML
1.  Busca: `<h1>Prueba</h1>`.
2.  Si el texto "Prueba" aparece en grande (formato título), significa que el HTML se está interpretando.

### Paso 3: Ejecución de JavaScript
1.  Intenta inyectar un script simple.
2.  Payload:
    ```html
    <script>alert('XSS')</script>
    ```
3.  Pulsa Buscar.

## 🏁 Verificación
*   Debería aparecer una ventana emergente (alert) con el texto "XSS".
*   Esto confirma que cualquier script enviado en la URL será ejecutado por el navegador.

## 🛡️ Preguntas de Reflexión
1.  ¿Cómo podría un atacante usar esto contra otro usuario? (Pista: Enlaces maliciosos).
2.  ¿Qué diferencia hay entre este XSS y el Stored?

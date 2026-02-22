# 🎓 Cadel Academy - Entorno de Entrenamiento en Ciberseguridad

**Cadel Academy** es una plataforma web educativa diseñada intencionalmente con vulnerabilidades de seguridad para el aprendizaje y práctica de **Auditoría Web** y **Hacking Ético**.

El proyecto simula una academia online funcional (con foro, chat, perfiles de usuario, blog, etc.) que permite a los estudiantes explorar, explotar y entender vulnerabilidades web comunes en un entorno seguro y controlado.

## 🚀 Arquitectura

La aplicación implementa una arquitectura dual única utilizando **Docker Compose**:

*   **Modo Vulnerable (Puerto 8080):** La aplicación se ejecuta sin protecciones, permitiendo ataques como SQL Injection, XSS, RCE, etc.
*   **Modo Seguro (Puerto 8443):** La misma aplicación, pero protegida tras un proxy inverso **Nginx** con HTTPS, cabeceras de seguridad y código sanitizado.

Un **interruptor en la interfaz** permite cambiar entre ambos modos en tiempo real para comparar el comportamiento.

## 🛠️ Instalación y Ejecución

### Prerrequisitos
*   Docker y Docker Compose instalados.
*   OpenSSL (generalmente preinstalado en Linux/Mac, necesario para generar certificados HTTPS).

### Pasos de Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/CADEL-WEB-AUDIT.git
    cd CADEL-WEB-AUDIT
    ```

2.  **Generar Certificados SSL:**
    Para habilitar el modo seguro (HTTPS), ejecuta el script de generación de certificados:
    ```bash
    ./scripts/generate_certs.sh
    ```
    *(Si estás en Windows y no tienes bash, puedes usar openssl manualmente o WSL).*

3.  **Levantar el entorno:**
    ```bash
    docker-compose up --build
    ```

4.  **Acceder a la plataforma:**
    *   Abre tu navegador y ve a: **http://localhost:8080**
    *   Para ver la versión segura: **https://localhost:8443** (Acepta la advertencia de certificado autofirmado).

## 👤 Credenciales por Defecto

La base de datos se inicializa automáticamente con los siguientes usuarios para pruebas:

| Usuario | Contraseña | Rol | Descripción |
| :--- | :--- | :--- | :--- |
| **admin** | `admin123` | Admin | Administrador del sistema. |
| **profesor** | `profesor123` | User | Docente de la academia. |
| **alumno** | `1234` | User | Estudiante estándar. |
| **hacker** | `hacker123` | User | Usuario malicioso simulado. |

## 🎯 Ejercicios de Auditoría

Explora las siguientes vulnerabilidades implementadas en el sistema:

### 1. SQL Injection (SQLi)
*   **Ubicación:** Formulario de Login (`/login`) y Buscador de Chat (`/chat`).
*   **Objetivo:** Iniciar sesión como administrador sin contraseña o extraer datos de usuarios.
*   **Payload:** `admin' OR '1'='1`

### 2. Cross-Site Scripting (XSS)
*   **Reflected:** En el buscador principal (`/search`).
*   **Stored:** En el Foro (`/forum`), Chat (`/chat`) y Perfil de Usuario (`/profile`).
*   **Objetivo:** Ejecutar JavaScript en el navegador de otro usuario (ej. `alert(1)` o robo de cookies).

### 3. Unrestricted File Upload (RCE)
*   **Ubicación:** Formulario de creación de temas en el Foro.
*   **Objetivo:** Subir un archivo con extensión peligrosa (ej. `.html` con JS o scripts de servidor) y ejecutarlo.

### 4. Gestión de Sesiones Insegura
*   **Ubicación:** Toda la aplicación.
*   **Objetivo:** Interceptar cookies de sesión (falta de flags `HttpOnly` y `Secure` en modo vulnerable).

### 5. Reconocimiento (Information Disclosure)
*   **Ubicación:** `robots.txt` y rutas ocultas.
*   **Objetivo:** Encontrar archivos de configuración sensibles usando herramientas como `nmap` o `dirb`.

## 📂 Estructura del Proyecto

```text
CADEL-WEB-AUDIT/
├── app/                # Código fuente de la aplicación (Flask)
│   ├── routes/         # Lógica vulnerable vs segura
│   ├── templates/      # Vistas HTML (Jinja2)
│   └── static/         # CSS, JS e imágenes
├── docker/             # Configuración de Docker y Nginx
├── docs/               # Documentación detallada de vulnerabilidades
├── LABs/               # Guías paso a paso para realizar los ejercicios
└── scripts/            # Scripts de utilidad (generación de certificados)
```

---
**⚠️ ADVERTENCIA:** Este software es **INSEGURO POR DISEÑO**. Contiene vulnerabilidades graves que permiten la ejecución remota de código y el compromiso del sistema. **NO LO DESPLIEGUES** en un servidor público accesible desde Internet. Úsalo únicamente en entornos locales controlados para fines educativos.
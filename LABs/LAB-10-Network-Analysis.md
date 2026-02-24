# Laboratorio 10: Análisis de Tráfico de Red (Wireshark)

## 🎯 Objetivo
Comprender la importancia del cifrado en las comunicaciones web interceptando tráfico real. Analizarás la diferencia entre HTTP y HTTPS y aprenderás a detectar firmas de ataques (SQLi/XSS) en los paquetes de red.

## 📋 Prerrequisitos
1.  **Wireshark** instalado en tu máquina anfitriona.
2.  Entorno Cadel Academy corriendo.
3.  Navegador Web.

---

## 📝 Ejercicio 1: Interceptación de Credenciales (Cleartext)

**Escenario:** Un atacante está escuchando en la red local. Un usuario inicia sesión en la versión no segura de la academia.

### Paso 1: Configurar Wireshark
1.  Abre Wireshark.
2.  Selecciona la interfaz de red correcta:
    *   **Linux:** `docker0` (si atacas desde el host al contenedor) o `any`.
    *   **Windows/Mac:** `Adapter for loopback traffic capture` (si accedes a localhost).
3.  Inicia la captura (icono de aleta de tiburón azul).
4.  En la barra de filtros (arriba), escribe: `http.request.method == "POST"` y pulsa Enter.

### Paso 2: Generar Tráfico
1.  Ve a `http://localhost:8080/login` (Modo Vulnerable).
2.  Inicia sesión con usuario: `admin` y contraseña: `supersecreto123`.

### Paso 3: Análisis
1.  Vuelve a Wireshark. Deberías ver un paquete capturado.
2.  Haz doble clic en el paquete.
3.  Despliega la sección **Hypertext Transfer Protocol** -> **HTML Form URL Encoded**.
4.  **Resultado:** Verás `username: admin` y `password: supersecreto123` en texto plano. ¡Has robado las credenciales!

---

## 📝 Ejercicio 2: Análisis de Ataques (Blue Team)

**Escenario:** Eres un analista de seguridad (SOC) buscando evidencias de un ataque reciente.

### Paso 1: Preparar la Captura
1.  Limpia la captura actual o inicia una nueva.
2.  Filtro: `http contains "UNION"` o `http contains "script"`.

### Paso 2: Simular el Ataque
1.  Ve al Buscador del Chat (`http://localhost:8080/chat`).
2.  Lanza una inyección SQL: `' UNION SELECT 1, @@version -- -`.

### Paso 3: Análisis Forense
1.  Observa que Wireshark ha capturado el paquete.
2.  Al inspeccionarlo, puedes ver claramente el payload malicioso en la URL o el cuerpo de la petición.
3.  **Conclusión:** Los IDS/IPS (Sistemas de Detección de Intrusos) funcionan así, buscando estos patrones en el tráfico para bloquearlos.

---

## 📝 Ejercicio 3: La Protección de HTTPS

**Objetivo:** Verificar que el cifrado protege los datos.

1.  Inicia una nueva captura en Wireshark.
2.  Ve a la versión segura: `https://localhost:8443/login`.
3.  Inicia sesión.
4.  Intenta filtrar por `http`. No verás nada (o muy poco).
5.  Filtra por `tcp.port == 8443`. Verás paquetes `TLSv1.3`.
6.  Intenta leer el contenido ("Application Data").
7.  **Resultado:** Todo son bytes ilegibles. Sin la clave privada del servidor, es imposible robar las credenciales.

---

## 🛡️ Preguntas de Reflexión

1.  ¿Por qué es peligroso usar Wi-Fi público sin VPN o HTTPS?
2.  ¿Puede Wireshark descifrar el tráfico HTTPS si tienes la clave privada del servidor (`server.key`)?
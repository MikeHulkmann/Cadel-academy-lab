#!/bin/bash

# Obtener la ruta absoluta del directorio donde está este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$SCRIPT_DIR/../docker/certs/server.key" \
    -out "$SCRIPT_DIR/../docker/certs/server.crt" \
    -subj "/C=ES/ST=Madrid/L=Madrid/O=CadelAudit/OU=IT/CN=localhost"

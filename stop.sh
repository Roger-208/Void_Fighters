#!/bin/bash

cd ./projecte_docker

echo "Parant servidor Void Fighters"

# Intentem avisar al servidor per TCP (només localhost). Si falla, continuem igual.
python3 - <<'PY' || true
import socket
try:
	s = socket.create_connection(('127.0.0.1', 65432), timeout=2)
	s.sendall(b'{"action":"stop_server"}\n')
	s.close()
except Exception:
	pass
PY

docker compose down --rmi all --remove-orphans

echo "Servidor Parat"

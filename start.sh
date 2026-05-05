#!/bin/bash

cd ./projecte_docker

echo "Iniciant servidor Void Fighters"

{
docker compose up --build
} || {
echo -e "\033[1mLa posada en funcionament ha fallat"
exit 1
}

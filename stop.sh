#!/bin/bash

cd ./projecte_docker

echo "Parant servidor Void Fighters"

docker compose down --rmi all --remove-orphans

echo "Servidor Parat"

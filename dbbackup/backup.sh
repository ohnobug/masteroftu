#!/bin/bash

docker exec -it masteroftu-mariadb-1 mysqldump -u root -pTurcarai2025 tur > tur.sql
docker exec -it masteroftu-mariadb-1 mysqldump -u root -pTurcarai2025 bitnami_moodle > bitnami_moodle.sql

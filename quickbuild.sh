#!/bin/bash

export buildfrontend="cd frontend/ && ./dockerbuild05.sh && cd .."
# export rebuild="docker compose -f docker-compose05.yml build newmoodle_api && docker compose -f docker-compose05.yml down newmoodle_api && docker compose -f docker-compose05.yml up newmoodle_api -d"
export rebuild="docker compose -f docker-compose05.yml build && docker compose -f docker-compose05.yml down && docker compose -f docker-compose05.yml up -d"

eval $buildfrontend
eval $rebuild
docker logs -f masteroftu-newmoodle_api-1
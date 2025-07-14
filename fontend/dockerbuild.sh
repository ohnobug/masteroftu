#!/bin/bash

docker run --rm -it -v ${PWD}:/app --workdir /app node:current-alpine3.22 yarn
docker run --rm -it -v ${PWD}:/app --workdir /app node:current-alpine3.22 yarn build
rm -rf ../nginx/static-files
mv ./dist ../nginx/static-files
chmod -R 777 ../nginx/static-files
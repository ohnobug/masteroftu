#!/bin/bash

find -type f -name "*.jsx" -exec sed -i "s/图克教育/智能客服/g" {} \;
find -type f -name "*.html" -exec sed -i "s/图克教育/智能客服/g" {} \;
docker run --rm -it -v ${PWD}:/app -e VITE_API_BASE_URL=http://192.168.0.5 -e VITE_WS_BASE_URL=http://192.168.0.5 --workdir /app node:current-alpine3.22 yarn
docker run --rm -it -v ${PWD}:/app -e VITE_API_BASE_URL=http://192.168.0.5 -e VITE_WS_BASE_URL=http://192.168.0.5 --workdir /app node:current-alpine3.22 yarn build
rm -rf ../nginx/static-files
mv ./dist ../nginx/static-files
chmod -R 777 ../nginx/static-files

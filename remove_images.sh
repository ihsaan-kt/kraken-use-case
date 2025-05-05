#!/bin/bash

docker stop $(docker ps -aq)
docker rmi -f $(docker images -aq) 2>/dev/null || true
docker volume rm $(docker volume ls -q)
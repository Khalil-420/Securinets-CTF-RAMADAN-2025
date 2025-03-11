#!/bin/bash

docker build -t chal01289342 .
docker run -d -p 1333:1333 --privileged chal01289342

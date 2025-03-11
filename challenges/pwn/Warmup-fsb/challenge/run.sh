#!/bin/bash

docker build -t chal01289341 .
docker run -d -p 1339:1339 --privileged chal01289341

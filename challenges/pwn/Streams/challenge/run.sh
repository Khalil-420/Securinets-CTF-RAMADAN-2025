#!/bin/bash

docker build -t chal01289343 .
docker run -d -p 1335:1335 --privileged chal01289343

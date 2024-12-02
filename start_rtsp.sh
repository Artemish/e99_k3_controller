#!/usr/bin/env bash

cd rstp-simple-server
docker run --rm -it -v $PWD/rtsp-simple-server.yml:/rtsp-simple-server.yml -p 7070:8554 aler9/rtsp-simple-server:v1.3.0

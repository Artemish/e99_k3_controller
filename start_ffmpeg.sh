#!/usr/bin/env bash

ffmpeg -re -stream_loop -1 -i /dev/video0 -f rtsp -rtsp_transport tcp rtsp://localhost:7070/webcam

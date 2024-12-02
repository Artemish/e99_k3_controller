## E99 K3 Pro controller

This project aims to allow controlling of many inexpensive quadcopters
(The E99 K3 Pro, ~ $14) for the purposes of budget drone swarm
testing.

### Laptop -> Drone Control

You can run the drone control software to control the drone from your
laptop. 

```bash
python3 drone_control_2.py
```

This should attempt to connect to the drone at the address
`192.168.1.1` and issue it a basic sequence of takeoff and landing
commands.

### Spoofing the drone (Deprecated)

Included are several scripts for mimicing functions of the drone so
that you can connect the controller to your laptop and observe the
control messages sent by the controller.

1. `start_rtsp.sh` starts a docker container running an RTSP server
   for emulating the drone's webcam
2. `start_ffmpeg.sh` streams your webcam to the RTSP docker server
3. `udp_controller.py` will listen for UDP messages from the
   controller and display updated data while you press buttons.

You can see an annotated control scheme log of the UDP protocol over
port 7099 [here](udp_control_log.txt)

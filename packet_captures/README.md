In this directory is an assortment of the packet captures used during
the development of this drone control program. They are mostly
unannotated, though I will include a brief summary of how and when
they were collected:

*app_to_laptop.pcapng*: Large collection of smartphone app to laptop
cloning the drone's WiFi hotspot

*controller_port_7099.pcapng*: Single packet of Controller to Drone
mesages (0101 on port 7099), appears to be an "all green" message of
some kind. Saved as single packet capture for replaying with Scapy.

*controller_port_8800.pcap*: Collection of Controller to the Drone's
alternate address *192.168.169.1* on port 8800

*Drone_experiment.pcap*: Collection of messages sent during an
experiment of the following flight plan implemented on the app for the
purposes of replaying a sample flight plan. The following steps occur
at the following times:

Setup: Close KY Ufo, start packet capture app

```
00: Start stopwatch, start packet capture
10: Start the KY UFO app
20: Start the drone
30: Connect to drone wifi
50: Touch calibration button
60: Turn on throttle controls in the app
70: Press the one-touch takeoff, then press the one-touch landing
```

*PCAPdroid_02_Dec_13_46_06.pcap*: Capture of controller and drone
traffic collected directly from the smartphone app (KY UFO) using the
Android capture app *PCAPdroid*. 

*rtsp-traffic.pcapng*: Collection of RTSP (webcam) TCP traffic (laptop
connected to drone WiFi)

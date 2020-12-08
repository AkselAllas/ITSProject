# ITSProject

## Main plan
- Use Parrot 2 camera feed to detect humans and their distance from camera real time.
- Use some algorithm for drone pathfinding, which avoids collision with humans.

## Requirements

- Python 3.4 or newer: 3.7 and 3.8 work fine
- OpenCV 3.4 - install with `pip3 install -Iv opencv-contrib-python=3.4.11.45`
- Pyardrone library: `pip3 install pyardrone`

## python-ardrone library - not in use

### Docker instructions
```
apt install python3 python3-pip libavcodec-dev libavformat-dev libswscale-dev
python3 install pillow
./setup.py install
```

*) Everytime you want restart drone battery, you have to reconnect to the ARDRONE wifi with your laptop.

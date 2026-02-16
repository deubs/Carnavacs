https://www.armbian.com/orange-pi-zero-3/

# Habilitar I2C3 / UART5
orangepi-config --> system --> hardware

# INSTALL
apt update
python3-serial
python3-evdev
python3-smbus
python3-dev
python3-setuptools
python3-requests
python3-structlog
swig
pip install python-socketio[client] websocket-client
Ir a /usr/src/wiringOP-Python
sudo su
python3 generate-bindings.py > bindings.i
python3 setup.py install

# I2C3
i2cdetect -y 3

# Checklan
Checklan needs target ip to be hardcoded.
Current target ip (server) is 192.168.40.251

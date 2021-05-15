#!/bin/bash
#
# HackServ installer
# install.sh
#
echo "This Script will install Hackserv as a Systemd Service."
echo "Creating 'HackServ' user..."
sudo useradd -s /bin/nologin hackserv
echo "Hiding hackserv.py in /usr/local/bin/..."
sudo cp hackserv.py /usr/local/bin/.hackserv.py
echo "Copying hsConfig.py to /usr/local/bin/..."
sudo cp hsConfig.py /usr/local/bin/hsConfig.py
sudo vim /usr/local/bin/hsConfig.py
echo "Copying hackserv.service to /etc/systemd/system..."
sudo cp hackserv.service /etc/systemd/system/hackserv.service
echo "Starting HackServ..."
sudo systemctl enable --now hackserv.service
echo "Done."

#!/bin/bash
#
# HackServ installer
# install.sh
#
echo "This Script will install Hackserv as a Systemd Service."
echo "Creating 'HackServ' user..."
sudo useradd -s /bin/nologin hackserv
echo "copying hackserv.py to /usr/local/bin/..."
sudo cp hackserv.py /usr/local/bin/.hackserv.py
echo "copying hsConfig.py to /usr/local/bin/..."
sudo cp hsConfig.py /usr/local/bin/hsConfig.py
echo "copying hackserv.service to /etc/systemd/system..."
sudo cp hackserv.service /etc/systemd/system/hackserv.service
echo "Starting HackServ..."
sudo systemctl enable --now hackserv.service
echo "Done."

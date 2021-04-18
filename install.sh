#!/bin/bash
#
# HackServ installer
# install.sh
#
sudo cp hackserv.py /usr/local/bin/.hackserv.py
sudo cp hsConfig.py /usr/local/bin/hsConfig.py
sudo cp hackserv.service /etc/systemd/system/hackserv.service
sudo systemctl enable --now hackserv.service
echo "Done."

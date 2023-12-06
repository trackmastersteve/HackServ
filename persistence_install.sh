#!/bin/bash
#
# HackServ installer
# install.sh
#
# Copyright (c) 2018-2024 Stephen Harris <trackmastersteve@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

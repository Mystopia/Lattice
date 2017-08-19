#! /bin/bash
# Installs current Nodejs on a raspberry pi.
# From http://thisdavej.com/beginners-guide-to-installing-node-js-on-a-raspberry-pi/
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt install nodejs vim supervisor -y


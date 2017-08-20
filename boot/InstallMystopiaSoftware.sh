#! /bin/bash
# Sets up a new Mystopia RPi by doing the following:
# - Installs needed packages.
# - Creates the Mystopia directory and installs needed apps from github.
# - Runs SetupMystopiaPi.sh at end.

set -ex

# Install base packages
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt install nodejs vim supervisor jq -y


# Install Mystopia applications and dependencies
mkdir -p /home/pi/Mystopia

git clone https://github.com/Mystopia/Lattice.git /home/pi/Mystopia/Lattice
git clone https://github.com/Mystopia/RCCControl.git /home/pi/Mystopia/RCCControl
cd /home/pi/Mystopia/RCCControl
npm install

git clone -b develop https://github.com/Mystopia/fadecandy.git /home/pi/Mystopia/fadecandy
cd /home/pi/Mystopia/fadecandy/server
make submodules && make


# Set up autostart, hostname
/boot/SetupMystopiaPi.sh

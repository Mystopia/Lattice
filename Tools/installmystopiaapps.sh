#! /bin/bash
# Creates the Mystopia directory and installs needed apps from github.


mkdir -p /home/pi/Mystopia

git clone https://github.com/Mystopia/fadecandy.git /home/pi/Mystopia/fadecandy
git clone https://github.com/Mystopia/Lattice.git /home/pi/Mystopia/Lattice
git clone https://github.com/Mystopia/RCCControl.git /home/pi/Mystopia/RCCControl


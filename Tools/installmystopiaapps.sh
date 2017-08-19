#! /bin/bash
# Creates the Mystopia directory and installs needed apps from github.


mkdir -p ~/Mystopia && cd ~/Mystopia

git clone https://github.com/Mystopia/fadecandy.git fadecandy
git clone https://github.com/Mystopia/Lattice.git Lattice
git clone https://github.com/Mystopia/RCCControl.git RCCControl


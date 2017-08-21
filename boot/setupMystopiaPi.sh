#! /bin/bash
# Sets up a new Mystopia RPi by doing the following:
# - Sets up LXDE autostart.
# - Sets new hostname from /boot/hardware-config.json's "hostname" key.
# - Reboots.
set -ex

# Set up LXDE autostart
cp /boot/scripts/autostart /home/pi/.config/lxsession/LXDE-pi/autostart

# Set hostname
#hostn=$(cat /etc/hostname)
#echo "Existing hostname is $hostn."
hostn=`hostname`
newhost=`jq --raw-output '.hostname' /boot/configs/hardware-config.json`
echo "Changing hostname to $newhost."
sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "Your new hostname is $newhost"


#Press a key to reboot
read -s -n 1 -p "Installation complete. Press any key to reboot."
sudo reboot

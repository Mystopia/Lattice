#! /bin/bash
# Sets up a new Mystopia RPi by doing the following:
# - Sets up LXDE autostart.
# - Sets new hostname from /boot/hardware-config.json's "hostname" key.
# - Reboots.
set -ex

# Set up supervisor
sudo ln -s /boot/supervisord.conf /etc/supervisor/conf.d/mystopia.conf
sudo cp /boot/supervisord.service /etc/systemd/system/
alias supervisorctl="supervisorctl -c /boot/supervisord.conf"
sudo systemctl enable supervisord.service
sudo systemctl start supervisord.service


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

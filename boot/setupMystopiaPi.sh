#! /bin/bash
# Sets up a new Mystopia RPi by doing the following:
# - Installs needed packages.
# - Creates the Mystopia directory and installs needed apps from github.
# - Sets up supervisord.
# - Sets new hostname from /boot/hardware-config.json's "hostname" key.
# - Reboots.


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


# Set up supervisor
sudo ln -s /etc/supervisor/conf.d/mystopia.ini /boot/supervisord.conf
sudo cp /boot/supervisord.service /etc/systemd/system/
alias supervisorctl="supervisorctl -c /boot/supervisord.conf"
sudo systemctl enable supervisord.service
sudo systemctl start supervisord.service


# Set hostname
echo "Existing hostname is $hostn."
newhost=$(jq '.hostname' /boot/hardware-config.json )
echo "Changing hostname to $newhost."
sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "Your new hostname is $newhost"


#Press a key to reboot
read -s -n 1 -p "Installation complete. Press any key to reboot."
sudo reboot

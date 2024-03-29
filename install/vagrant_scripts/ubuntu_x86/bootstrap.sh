#!/usr/bin/env bash
echo "Makahiki Environment Setup Script for Ubuntu (x86)"
echo "--------------------------------------------------"
echo "Script started at $(date)"
echo "Appending locale settings (UTF-8) to /etc/bash.bashrc: started at $(date)"
echo "# UTF-8 locale settings for Makahiki" >> /etc/bash.bashrc
echo "export LANGUAGE=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LANG=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc
echo "Appending locale settings (UTF-8): finished at $(date)"
echo "Configuring UTF-8 locale settings: started at $(date)"
locale-gen en_US.UTF-8
dpkg-reconfigure locales
echo "Configuring UTF-8 locale settings: finished at $(date)"
echo "Updating package list: started at $(date)"
echo "apt-get update"
apt-get update
echo "Updating package list: finished at $(date)"
echo "Installing git: started at $(date)"
echo "apt-get install -y git"
apt-get install -y git
echo "Installing git: finished at $(date)"
echo "Installing gcc: started at $(date)"
echo "apt-get install -y gcc"
apt-get install -y gcc
echo "Installing gcc: finished at $(date)"
echo "Installing python-setuptools: started at $(date)"
echo "apt-get install -y python-setuptools"
apt-get install -y python-setuptools
echo "Installing python-setuptools: finished at $(date)"
echo "Installing pip: started at $(date)"
echo "easy_install pip"
easy_install pip
echo "Installing pip: finished at $(date)"
echo "Installing python-imaging: started at $(date)"
echo "apt-get install -y python-imaging"
apt-get install -y python-imaging
echo "Installing python-imaging: finished at $(date)"
echo "Installing python-dev: started at $(date)"
echo "apt-get install -y python-dev"
apt-get install -y python-dev
echo "Installing python-dev: finished at $(date)"
echo "Installing libjpeg-dev: started at $(date)"
echo "apt-get install -y libjpeg-dev"
apt-get install -y libjpeg-dev
echo "Installing libjpeg-dev: finished at $(date)"
# Python Imaging Library shared library symlink setup
echo "Configuring Python Imaging Library shared libraries: started at $(date)"
if [ ! -f /usr/lib/libjpeg.so ]
    then
        if [ -f /usr/lib/i386-linux-gnu/libjpeg.so ]
            then
                echo "Found: /usr/lib/i386-linux-gnu/libjpeg.so"
                echo "Creating symlink: /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so"
                echo "sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so"
                sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/
            else
                echo "Could not find libjpeg.so in /usr/lib or /usr/lib/i386-linux-gnu/." 
                echo "Python Imaging Library packages may not have installed properly."
                echo "Script exiting at $(date)."
                exit 1
                fi
    else
        echo "Found: /usr/lib/libjpeg.so"
fi

if [ ! -f /usr/lib/libz.so ]
    then
        if [ -f /usr/lib/i386-linux-gnu/libz.so ]
            then
                echo "Found: /usr/lib/i386-linux-gnu/libz.so"
                echo "Creating symlink: /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so"
                echo "sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/"
                sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/
            else
                echo "Could not find libz.so in /usr/lib or /usr/lib/i386-linux-gnu/."
                echo "Python Imaging Library packages may not have installed properly."
                echo "Script exiting at $(date)"
                exit 1
        fi
    else
        echo "Found: /usr/lib/libz.so"
fi
echo "Configuring Python Imaging Library shared libraries: finished at $(date)"
echo "Installing postgresql-9.1: started at $(date)"
echo "apt-get install -y postgresql-9.1"
apt-get install -y postgresql-9.1
echo "Installing postgresql-9.1: finished at $(date)"
echo "Installing libpq-dev: started at $(date)"
echo "apt-get install -y libpq-dev"
apt-get install -y libpq-dev
echo "Installing libpq-dev: finished at $(date)"
echo "Configuring PostgreSQL cluster \"main\" with locale en_US.UTF8: started at $(date)"
echo "pg_dropcluster 9.1 main --stop"
pg_dropcluster 9.1 main --stop
echo "pg_createcluster --locale en_US.UTF8 9.1 main"
pg_createcluster --locale en_US.UTF8 9.1 main
echo "Configuring PostgreSQL cluster \"main\" with locale en_US.UTF8: finished at $(date)"
echo "Installing memcached: started at $(date)"
echo "apt-get install -y memcached"
apt-get install -y memcached
echo "Installing memcached: finished at $(date)"
echo "Installing libmemcached-dev: started at $(date)"
echo "apt-get install -y libmemcached-dev"
apt-get install -y libmemcached-dev
echo "Installing libmemcached-dev: finished at $(date)"
echo "Installing virtualenvwrapper: started at $(date)"
echo "pip install virtualenvwrapper"
pip install virtualenvwrapper
echo "Installing virtualenvwrapper: finished at $(date)"
echo "Appending virtualenvwrapper settings to /home/vagrant/.bashrc: started at $(date)"
echo "# Virtualenvwrapper settings for makahiki" >> /home/vagrant/.bashrc
echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
echo "export PROJECT_HOME=/home/vagrant/makahiki" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
echo "Appending virtualenvwrapper settings to /home/vagrant/.bashrc: finished at $(date)"
echo "Downloading source code from Github: started at $(date)"
echo "cd /home/vagrant"
cd /home/vagrant
# This line needs to be changed before merging with the main repository
echo "git clone http://github.com/jtakayama/makahiki"
git clone http://github.com/jtakayama/makahiki.git
echo "chown -R vagrant:vagrant /home/vagrant/makahiki"
chown -R vagrant:vagrant /home/vagrant/makahiki
echo "Downloading source code from Github: finished at $(date)"
echo "Script completed at $(date)"
exit 0
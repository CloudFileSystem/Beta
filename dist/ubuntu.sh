#!/bin/bash

#
# install python setuptools
#
sudo apt-get -y install python-setuptools
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev

#
# install FUSE
#
sudo apt-get -y install fuse
sudo apt-get -y install libfuse-dev

#
# install MySQL
#
sudo apt-get -y install mysql-client mysql-server mysql-dev
sudo apt-get -y install libmysqlclient-dev

#
# install pip
#
sudo easy_install pip

#
# install virtualenv
#
sudo pip install fuse-python
sudo pip install fusepy
sudo pip install sqlalchemy
sudo pip install MySQL-python

# vim: set nu ts=2 autoindent : #


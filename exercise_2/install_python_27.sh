#!/bin/bash

sudo yum install python27-devel -y
mv /usr/bin/python /usr/bin/python266
ln -s /usr/bin/python2.7 /usr/bin/python
python --version

# Install ez_setup and pip
sudo curl -o ez_setup.py https://bootstrap.pypa.io/ez_setup.py
sudo python ez_setup.py
sudo /usr/bin/easy_install-2.7 pip
sudo pip install virtualenv

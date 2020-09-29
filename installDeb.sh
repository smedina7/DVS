#!/bin/bash

# do we need to chmod manually of install.sh before running it?
#chmod +x install.sh

#Update
echo "Running apt-get update"
apt-get -y update




### Install dependencies
#
REQUIRED_PROGRAMS="python3-pip python3-venv git"
REQUIRED_PYTHON_PACKAGES="PyQt5 plotly dash Flask pandas"

echo "+++++++++++++++++++++++++++++++++"
echo "installing REQUIRED_PROGRAMS"
if [ -x "/usr/bin/apt-get" ]; then
    OS_VERSION="Debian"
    apt-get -y install $REQUIRED_PROGRAMS
elif [ -x "/usr/bin/yum" ]; then
    OS_VERSION="CentOS"
    yum install -y $REQUIRED_PROGRAMS
else
    echo "$OUTPUT_ERROR_PREFIX Distribution not supported"
    exit 1
fi

### Installing python3 dependencies
echo "+++++++++++++++++++++++++++++++++"
echo "installing REQUIRED_PYTHON_PACKAGES"
pip install pip --upgrade
pip install $REQUIRED_PYTHON_PACKAGES

pip3 install pip --upgrade
pip3 install $REQUIRED_PYTHON_PACKAGES
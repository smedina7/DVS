#!/bin/bash

# do we need to chmod manually of install.sh before running it?
#chmod +x install.sh

set -e

ECEL_NETSYS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Update
echo "Running apt-get update"
apt-get -y update

### Helper functions
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case $yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}

#Installing Wireshark
ECELD_DEPS="eceld-wireshark"
for eceld_dep in $ECELD_DEPS; do
    eceld_prompt="$eceld_dep found, remove it and reinstall?"
    if [ -d $ECEL_NETSYS_DIR/$eceld_dep ]; then
        if prompt_accepted_Yn "$eceld_prompt"; then
            rm $ECEL_NETSYS_DIR/$eceld_dep -rf
        git clone https://github.com/ARL-UTEP-OC/$eceld_dep "$ECEL_NETSYS_DIR"/$eceld_dep
        pushd "$ECEL_NETSYS_DIR"/$eceld_dep
        chmod +x install.sh
        ./install.sh
        popd
        fi
    else
        eceld_prompt="$eceld_dep not found, download and install?"
        if prompt_accepted_Yn "$eceld_prompt"; then
            rm $ECEL_NETSYS_DIR/$eceld_dep -rf
        git clone https://github.com/ARL-UTEP-OC/$eceld_dep "$ECEL_NETSYS_DIR"/$eceld_dep
        pushd "$ECEL_NETSYS_DIR"/$eceld_dep
        chmod +x install.sh
        ./install.sh
        popd
        fi
    fi
done

for eceld_dep in $ECELD_DEPS; do
    if [ ! -d $ECEL_NETSYS_DIR/$eceld_dep ]; then
        echo "Download and installation of $eceld_dep not successful (can't execute program) quitting..."
        exit 1
    fi
done
##needs to be implemented

### Install dependencies
REQUIRED_PROGRAMS="python3-pip python3-venv git"
REQUIRED_PYTHON_PACKAGES="PyQt5==5.15.1 plotly dash Flask pandas flask_caching PyQtWebEngine virtualenv"

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

PYTHON_EXEC="python3"
### Create virtualenv if it doesn't currently exist
echo "+++++++++++++++++++++++++++++++++"
echo "$OUTPUT_PREFIX Installing python dependencies"
if [ ! -d "venv" ]; then
    $PYTHON_EXEC -m venv venv
fi

source venv/bin/activate
pip install pip --upgrade
pip install $REQUIRED_PYTHON_PACKAGES --use-feature=2020-resolver
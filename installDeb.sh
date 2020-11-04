#!/bin/bash


set -e

DVS_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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

DVS_DEPS="eceld-wireshark"
#Installing Wireshark
for dvs_dep in $DVS_DEPS; do
    dvs_prompt="DVS depends on : $dvs_dep would you like to install it"
    if prompt_accepted_Yn "$dvs_prompt"; then
        rm $DVS_DIRECTORY/$dvs_dep -rf
        git clone https://github.com/ARL-UTEP-OC/$dvs_dep "$DVS_DIRECTORY"/$dvs_dep
        pushd "$DVS_DIRECTORY"/$dvs_dep
        chmod +x install.sh
        ./install.sh
        popd
        for dvs_dep in $DVS_DEPS; do
            if [ ! -d $DVS_DIRECTORY/$dvs_dep ]; then
                echo "Download and installation of $dvs_dep not successful (can't execute program) quitting..."
                exit 1
            fi
        done
    else
        echo "Did not install: $dvs_dep . DVS depends on $dvs_dep to work properly. Please make sure it is installed. "
        echo "Please go to README to see installation requierements."
    fi
done





### Install dependencies
REQUIRED_PROGRAMS="python3-pip python3-venv git"
REQUIRED_PYTHON_PACKAGES="PyQt5==5.15.1 dash dash-bootstrap-components==0.10.7rc1 plotly Flask pandas flask_caching PyQtWebEngine virtualenv dash_daq"

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
# sudo pip install dash --use-feature=2020-resolver
# sudo pip install dash-bootstrap-components==0.10.7rc1 --use-feature=2020-resolver
sudo apt-get install -y python3-pyqt5.qtwebengine
sudo pip install $REQUIRED_PYTHON_PACKAGES --use-feature=2020-resolver
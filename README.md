# Data Visualization System (DVS)

## Table of Contents

* Data Visualization System (DVS)
  * [Description](https://github.com/smedina7/DVS#description)
  * [Installation](https://github.com/smedina7/DVS#installation)
    * [System Requirements](https://github.com/smedina7/DVS#system-requirements)
    * [Windows](https://github.com/smedina7/DVS#windows)
    * [Linux](https://github.com/smedina7/DVS#Linux)
* [Team Collaborators](https://github.com/smedina7/DVS#team-collaborators)
    
## Description
The purpose of the Data Visualization System is to provide the user with an integrated view of the data generated by the Evaluator Centric and Extensible Logger daemon (ECELd) and the ability to tag and modify the data associated with a capture taken by ECELd.  

## Installation

### System requirements
DVS runs on both Windows and Linux

#### Windows
DVS installation steps:
Open a command prompt in administrator mode and clone the repository. 

``` bash
> git clone https://github.com/smedina7/DVS
> cd dvs
```

Run the windows installer script. 

```bash
> win_installer.bat
```
You will get a prompt to install wireshark. Install using default settings provided and install in C:\Program Files\Wireshark.
After wireshark is installed, the script will do the following:

- Install Python’s Virtual Environment Builder
- Create and activate virtual environment
- Install required dependencies

After the installation is done you'll see the following message:
``` bash 
************************
All dependencies where installed successfully
run 'main.py --no-sandbox' to start DVS
```

Start the DVS GUI:
``` bash 
(dvs-venv) > python3 main.py --no-sandbox
```

Note: If you are unable to install wireshark through the command above mentioned, please go to this link: 
[DVS-wireshark installer](https://drive.google.com/drive/folders/1A4n18dsXHc-RHXywYPN-1mOt97gEFNq_?usp=sharing),
download the eceld-wireshark installer and install using default configurations.
Alternatively, you can download [eceld-wireshark](https://github.com/ARL-UTEP-OC/eceld-wireshark)
from their GitHub page, modify the files specified in the [documentation](https://github.com/smedina7/DVS/blob/master/documentation/DVS%20User%20Documentation.pdf), compile and build using the instructions found at the [Wireshark Win32/64: Step-by-Step Guide](https://www.wireshark.org/docs/wsdg_html_chunked/ChSetupWin32.html). 



#### Linux
**Requierements:**

Have Eceld-Wireshark installed: there are many ways you could install this. 
* Install Eceld-Netsys: Refer to the GitHub page -> https://github.com/ARL-UTEP-OC/eceld-netsys.git
* Install Eceld-Wireshark: Refer to the GitHub page -> https://github.com/ARL-UTEP-OC/eceld-wireshark
* Install with the DVS Installer 

DVS installation steps:

Clone the repo to your desired destination and go into the DVS folder: 

```bash
$ git clone https://github.com/smedina7/DVS
$ cd DVS
```

Install ECELD-Wireshark & Python3 dependencies into environment:

```bash
$ sudo ./installDeb.sh
```

When prompted:

```bash
kali@kali:~/DVS$ sudo ./installDeb.sh 
Running apt-get update
Hit:1 https://packages.microsoft.com/repos/vscode stable InRelease
Hit:2 http://kali.download/kali kali-rolling InRelease
Reading package lists... Done
DVS depends on : eceld-wireshark would you like to install it [Y/n] 
```
Input "Y" to install Eceld-Wireshark.

**If you already have Eceld-Wireshark installed, skip installation by inputing "n"**
NOTE: First time using the DVS System, you must follow the instructions located in the File -> Wireshark_mod_files


Activate Environment:

```bash
$ source venv/bin/activate
```

Run DVS:

```
$ sudo python3 main.py --no-sandbox
```






## Team Collaborators
  * Bianca Alvarez
  * Briana Sanchez
  * Dima AbdelJaber
  * Luisana Clarke
  * Rocio Cardona
  * Stephanie Medina

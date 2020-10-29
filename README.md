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

``` bash
> git clone https://github.com/smedina7/DVS
> cd dvs
```

Install eceld-wireshark using the installer provided. Type the following in the command prompt.

```bash
> nsis\Wireshark-win64-3.2.5.exe
```
You will get a prompt to install wireshark. Install using default settings provided.

- Install Python’s Virtual Environment Builder:
- Create and activate virtual environment:
- Install required dependencies:
``` bash
> pip install virtualenv
> virtualenv dvs-venv 
> dvs-venv\Scripts\activate
(dvs-venv) > pip install -r requirements.txt
```

Start the DVS GUI:

``` bash 
(dvs-venv) > main.py 
```

#### Linux
**Requierements:**

Have Eceld-Wireshark installed: there are many ways you could install this. 
* Install Eceld-Netsys: Refer to the Git-Hub page -> https://github.com/ARL-UTEP-OC/eceld-netsys.git
* Install Eceld-Wireshark: Refer to the Git-Hub page -> https://github.com/ARL-UTEP-OC/eceld-wireshark
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

Activate Environment:

```bash
$ source venv/bin/activate
```

Run DVS:

```
$ python3 main.py
```






## Team Collaborators
  * Bianca Alvarez
  * Briana Sanchez
  * Dima AbdelJaber
  * Luisana Clarke
  * Rocio Cardona
  * Stephanie Medina

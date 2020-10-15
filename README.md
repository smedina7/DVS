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
> eceld-wireshark-installer\Wireshark-win64-3.2.5.exe
```
You will get a prompt to install wireshark. Install using default settings provided.

- Install Python’s Virtual Environment Builder:
- Create and activate virtual environment:
- Install required dependencies:
``` bash
> pip install virtualenv
> python -m venv dvs-venv
> dvs-venv\Scripts\activate
(dvs-venv) > pip install -r requirements.txt
```

Start the DVS GUI:

``` bash 
(dvs-venv) > run-dvs.py 
```

#### Linux
##### To run in a Python virtual environment:

Clone the repo to your desired destination and go into the DVS folder: 

`git clone https://github.com/smedina7/DVS`

`cd dvs`

Install ECELD-Wireshark & Python3 dependencies into environment:

`sudo ./installDeb.sh`

Activate Environment:

`source venv/bin/activate`

Run DVS:

`bash run-dvs.sh`


## Team Collaborators
  * Bianca Alvarez
  * Briana Sanchez
  * Dima AbdelJaber
  * Luisana Clarke
  * Rocio Cardona
  * Stephanie Medina

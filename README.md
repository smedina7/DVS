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
To run in a Windows virtual environment:

`git clone https://github.com/smedina7/DVS`

`cd dvs`

Install Python’s Virtual Environment Builder:

`pip install virtualenv`

Create and activate virtual environment:

`python -m venv dvs-venv`

`dvs-venv\Scripts\activate`

Install required dependencies:
`pip install -r requirements.txt`

Start the DVS GUI:

`main.py`

#### Linux
##### To run in a Python virtual environment:

Clone the repo to your desired destination and go into the DVS folder: 

`git clone https://github.com/smedina7/DVS`
`cd dvs`

Install Python’s Virtual Environment Builder:

`pip install virtualenv`

Create and activate virtual environment:

`virtualenv venv`

`source venv/bin/activate`

Install required dependencies:
`pip install -r requirements.txt`

Start the DVS GUI:

`python3 main.py`

##### To run on your machine:

Clone the repo to your desired destination and go into the DVS folder: 

`git clone https://github.com/smedina7/DVS`
`cd dvs`

Install dependencies:

`sudo installDeb.sh`

Start the DVS GUI:

`python3 main.py`

## Team Collaborators
  * Bianca Alvarez
  * Briana Sanchez
  * Dima AbdelJaber
  * Luisana Clarke
  * Rocio Cardona
  * Stephanie Medina

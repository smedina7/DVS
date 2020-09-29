# Data Visualization System (DVS)

## Table of Contents

* Data Visualization System (RES)
  * [Description](https://github.com/smedina7/DVS#description)
  * [Installation](https://github.com/smedina7/DVS#installation)
    * [System Requirements](https://github.com/smedina7/DVS#system-requirements)
    * [Windows](https://github.com/smedina7/DVS#windows)
    * [Linux](https://github.com/smedina7/DVS#Linux)
  * [Team Collaborators](https://github.com/smedina7/DVS#team-collaborators)
    
## Description
The purpose of the Data Visualization System is to a tool that provides the user with an integrated view of the data generated by the Evaluator Centric and Extensible Logger daemon (ECELd) and the ability to tag and modify the data associated with a capture taken by ECELd.  

## Installation

### System requirements
DVS runs on both Windows and Linux

#### Windows
To run in a Windows virtual environment:

`git clone https://github.com/smedina7/DVS`

`cd dvs`

Install Python’s Virtual Environment Builder 

`pip install virtualenv`

Create and activate virtual environment:

`python -m venv dvs-venv`

`dvs-venv\Scripts\activate`

Install required dependencies:
`pip install -r requirements.txt`

Start the DVS GUI:

`main.py`


#### Linux

## Team Collaborators
  * Bianca Alvarez
  * Briana Sanchez
  * Dima AbdelJaber
  * Luisana Clarke
  * Rocio Cardona
  * Stephanie Medina

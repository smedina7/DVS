#for running on Windows env
import os
import subprocess

path = os.getcwd()

subprocess.Popen(["python", path+"/GUI/main.py"])
subprocess.Popen(["python", path+"/GUI/Widgets/WebEngineView.py"])
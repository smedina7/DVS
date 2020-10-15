#shut down server on Linux
import os
import signal

path = os.getcwd()
os.system("ps aux | grep WebEngineView >" +path+"/GUI/Dash/dash_pid.txt")

f = open(path+"/GUI/Dash/dash_pid.txt", 'r')

p = f.read().split()

pid = int(p[1])

os.kill(pid, signal.SIGTERM)
#shut down server on Linux
import os
import signal
import sys

path = os.getcwd()+"/GUI/Dash/dash_pid.txt"

try:
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system("ps aux | grep WebEngineView > " +path)
        f = open(path, 'r')
        p = f.read().split()
        pid = int(p[1])
        os.kill(pid, signal.SIGTERM)
    else:
        os.system("taskkill /IM QtWebEngineProcess.exe /F")
        #os.kill(signal.CTRL_C_EVENT, 0)
        
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.error('RunWebEngine(): Error during Web Engine termination')
    traceback.print_exception(exc_type, exc_value, exc_traceback)

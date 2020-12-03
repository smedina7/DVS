#shut down server on Linux
import os
import signal
import sys
import logging
import sys, traceback

path = os.path.abspath("GUI/PacketView/wireshark_pid.txt")

try:
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system("ps aux | grep wireshark > " +path)
        f = open(path, 'r')
        p = f.read().split()
        pid = int(p[1])
        try:
            os.kill(pid, signal.SIGTERM)
        except:
            print("All is closed")
    else:
        os.system("taskkill /IM wireshark.exe /F")
        #os.kill(signal.CTRL_C_EVENT, 0)
        
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.error('CloseWireshark(): Error during Wireshark termination')
    traceback.print_exception(exc_type, exc_value, exc_traceback)
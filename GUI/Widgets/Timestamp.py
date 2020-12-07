import os
class Timestamp:
    def __init__(self):
        throughput_file = 'GUI/Dash/timestamp.txt'
        if not os.path.exists(throughput_file):
            create = open(throughput_file, "w+")
            create.close()
        
    def update_timestamp(new_timestamp):
        ts = new_timestamp
        path = os.getcwd()+'/GUI/Dash/timestamp.txt'
        _file = open(path, 'w')
        _file.write(ts)
        _file.close()

    def get_current_timestamp():
        path = os.getcwd()+'/GUI/Dash/timestamp.txt'
        _file = open(path, 'r')
        currTimestamp = _file.readline()
        _file.close()
        return currTimestamp
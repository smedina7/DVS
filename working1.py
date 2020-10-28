import json
import sys
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QPushButton




if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    with open('test3/ParsedLogs/MouseClicks.JSON', 'r') as data_file:
        json_data = data_file.read()

    d = json.loads(json_data)
    # print("This is the json: ", d) debugging

    # d = json.loads(data)
    keyss = ["clicks_id", "content", "type", "classname", "start"]
    labels = keyss

    # print(len(labels))

    w = QtWidgets.QTableWidget(0, len(labels))
    # delegate = DateTimeDelegate(w)
    # w.setItemDelegateForColumn(0, delegate)
    # w.setColumnHidden(4, True)
    w.setHorizontalHeaderLabels(labels)


    df = pd.read_json (r'test3/ParsedLogs/MouseClicks.JSON')
    # print("This is a test", df)
    i = 0

    for ind in df.index: 
        # print(df['clicks_id'][ind], df['content'][ind]) 
        # it = QtWidgets.QTableWidgetItem()
        # it.setData(QtCore.Qt.DisplayRole, ind)
        # print(ind)
        c = 0
        j = 0
        clicks_id = str(ind)
        # print (type (clicks_id))
        w.insertRow(w.rowCount())
        for j in keyss:
            # print (type (df[j][ind]))
            # w.insertRow(w.rowCount())
            if j == "clicks_id":
                it = QtWidgets.QTableWidgetItem()
                it.setData(QtCore.Qt.DisplayRole, (clicks_id))
                # w.setItem(ind, c, it)
            else:
                it = QtWidgets.QTableWidgetItem()
                it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))
            # print (df[j][ind])
            w.setItem(ind, c, it)
            # print("ind:", ind, "c:", c, "it:", it)
            
            # print("row count",i, " ", w.rowCount)
            i = i + 1
            c= c+1

    btn= QtWidgets.QPushButton('Open')
    w.setCellWidget(0,1, btn)

  
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
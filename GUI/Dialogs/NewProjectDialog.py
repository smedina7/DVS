from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QTextEdit, QMessageBox, QSizePolicy, QAction, qApp, QLabel, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QKeyEvent, QTextCursor
import logging
import os
import sys
import shutil
from distutils.dir_util import copy_tree

from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

#PARSER
from GUI.Widgets.commentsParser import commentsParser

class NewProjectDialog(QtWidgets.QWidget):
    #Signal for when the user is done creating the new project
    created = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.folder_chosen = ''
        
        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("New Project")
        self.setObjectName("NewProjectDialog")

        #Label - New Project Title
        self.labelVerBoxPro = QtWidgets.QVBoxLayout()
        self.labelVerBoxPro.setObjectName("labeVerBoxPro")
        self.newProjectLabel = QLabel("Create New Project")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.newProjectLabel.setFont(labelFont)
        self.newProjectLabel.setAlignment(Qt.AlignCenter)

        self.nameVerBoxPro = QtWidgets.QHBoxLayout()
        self.nameVerBoxPro.setObjectName("nameVerBoxPro")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Type in New Project Name:")
        self.nameVerBoxPro.addWidget(self.nameLabel)
        self.project_name = QLineEdit()
        self.project_name.returnPressed.connect(self.on_create_clicked)
        ###### Fixed Height for project name text box
        self.project_name.setFixedHeight(27)

        #selected folder path
        self.pathHorBox = QtWidgets.QHBoxLayout()
        self.pathHorBox.setObjectName("pathHorBox")
        self.selectedpathLabel = QtWidgets.QLabel()
        self.selectedpathLabel.setObjectName("selectedpathLabel")
        self.selectedpathLabel.setText("Folder Selected:  ")

        self.pathLineEdit = QtWidgets.QLineEdit()
        self.pathLineEdit.setAcceptDrops(False)
        self.pathLineEdit.setReadOnly(True)
        self.pathLineEdit.setObjectName("pathLineEdit") 
        
        self.chooseFolderButton = QPushButton("Choose Folder")
        self.chooseFolderButton.clicked.connect(self.on_choose_button_clicked)
        
        #buttons
        self.create_project_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        #add on click events
        self.create_project_button.clicked.connect(self.on_create_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #put all components together
        self.labelVerBoxPro.addWidget(self.newProjectLabel)
        self.nameVerBoxPro.addWidget(self.project_name)
        self.pathHorBox.addWidget(self.selectedpathLabel)
        self.pathHorBox.addWidget(self.pathLineEdit)
        self.pathHorBox.addWidget(self.chooseFolderButton)
        self.bottomButtons_layout.addWidget(self.create_project_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

         #put all the components together
        self.outerVertBoxPro.addLayout(self.labelVerBoxPro)
        self.outerVertBoxPro.addLayout(self.nameVerBoxPro)
        self.outerVertBoxPro.addLayout(self.pathHorBox)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.setLayout(self.outerVertBoxPro)

    def on_create_clicked(self): 
        working_dir = os.getcwd()
        project_data_folder = os.path.join(working_dir, "ProjectData")
        if(not os.path.exists(project_data_folder)):
            os.mkdir(project_data_folder)
            
        self.project_data_path = os.path.join(project_data_folder, self.project_name.text())

        #set project path
        if self.project_name.text() == '':
            QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Project Name is Empty!",
                                        QMessageBox.Ok)

        
        elif os.path.exists(self.project_data_path) == True:
            QMessageBox.warning(self,
                                    "Name Exists",
                                    "The project name specified and directory already exists",
                                    QMessageBox.Ok)            
            return None

        else:
            #create dir
            os.mkdir(self.project_data_path)

            #copy selected dir to new dir
            self.batch_thread = BatchThread()
            self.batch_thread.progress_signal.connect(self.update_progress_bar)
            self.batch_thread.completion_signal.connect(self.copy_dir_complete)
            self.batch_thread.add_function(self.copy_dir, self.project_data_path)

            

            self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
            self.batch_thread.start()
            self.progress_dialog_overall.show()

            #BIANCA
            # #TRIGGER PACKET COMMENTS PARSER
            packetscomments_jsonpath = self.project_data_path 
            commentsParser(packetscomments_jsonpath)

    def copy_dir(self, dir):
        try:
            copy_tree(self.folder_chosen, dir)
        
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('copy_dir(): Error copying directory chosen')
            traceback.print_exception(exc_type, exc_value, exc_traceback)


    def copy_dir_complete(self):
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        #send signal to manager to start getting the files
        self.created.emit(self.project_data_path)
        self.close()

    def update_progress_bar(self):
        self.progress_dialog_overall.update_progress()
    
    def on_cancel_clicked(self, event):
        self.quit_event = event

        cancel = QMessageBox.question(
            self, "Close New Project",
            "Are you sure you want to cancel creating a new project?",
            QMessageBox.Close | QMessageBox.Cancel)

        if cancel == QMessageBox.Close:
            self.close()

        elif cancel == QMessageBox.Cancel:
            pass

    def on_choose_button_clicked(self):
        self.folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Project Directory to Analyze"))

        if self.folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(self.folder_chosen) > 0:
            self.folder_chosen = os.path.abspath(self.folder_chosen)
            self.pathLineEdit.setText(self.folder_chosen)
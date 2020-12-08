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
from GUI.PackageManager.PackageManager import PackageManager

#PARSER
from GUI.Widgets.commentsParser import commentsParser

#TAGS
from GUI.Widgets.textdataline import reloadDataline

class NewProjectDialog(QtWidgets.QWidget):
    #Signal for when the user is done creating the new project
    created = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.folder_chosen = ''
        self.file_chosen = ''
        
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

        self.zipHBox = QtWidgets.QHBoxLayout()
        self.zipHBox.setObjectName("zip_file")
        self.zip_file_label = QtWidgets.QLabel()
        self.zip_file_label.setObjectName("zipLabel")
        self.zip_file_label.setText("Import Zip File: ")
        self.zipHBox.addWidget(self.zip_file_label)

        self.zipLineEdit = QtWidgets.QLineEdit()
        self.zipLineEdit.setAcceptDrops(False)
        self.zipLineEdit.setReadOnly(True)
        self.zipLineEdit.setObjectName("zipLineEdit") 

        self.chooseFileButton = QPushButton("Choose File")
        self.chooseFileButton.clicked.connect(self.on_choosefile_button_clicked)

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
        self.import_project_button = QPushButton("Import")
        self.cancel_button = QPushButton("Cancel")

        #add on click events
        self.import_project_button.clicked.connect(self.import_zip)
        self.create_project_button.clicked.connect(self.on_create_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #put all components together
        self.labelVerBoxPro.addWidget(self.newProjectLabel)
        self.zipHBox.addWidget(self.zipLineEdit)
        self.zipHBox.addWidget(self.chooseFileButton)
        self.nameVerBoxPro.addWidget(self.project_name)
        self.pathHorBox.addWidget(self.selectedpathLabel)
        self.pathHorBox.addWidget(self.pathLineEdit)
        self.pathHorBox.addWidget(self.chooseFolderButton)
        self.bottomButtons_layout.addWidget(self.create_project_button)
        self.bottomButtons_layout.addWidget(self.import_project_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

         #put all the components together
        self.outerVertBoxPro.addLayout(self.labelVerBoxPro)
        self.outerVertBoxPro.addLayout(self.zipHBox)
        self.outerVertBoxPro.addLayout(self.nameVerBoxPro)
        self.outerVertBoxPro.addLayout(self.pathHorBox)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.setLayout(self.outerVertBoxPro)

    def import_zip(self):
        package_mgr = PackageManager()
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.unzip_complete)
        self.batch_thread.add_function(package_mgr.unzip, self.zip_to_import, self.file_name, self.project_data_folder)
        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

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

            
            try:
                # #TRIGGER PACKET COMMENTS PARSER
                datalinepath = self.project_data_path 
                commentsParser(datalinepath)

                #TAG
                reloadDataline.addTagColumn(datalinepath)

            except:
                print('Folder path not found')

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

    def unzip_complete(self):
        logging.debug("unzip_complete(): Instantiated")
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        self.created.emit(self.new_project_path)

        try:
            # #TRIGGER PACKET COMMENTS PARSER
            datalinepath = self.new_project_path 
            commentsParser(datalinepath)
            #TAG
            reloadDataline.addTagColumn(datalinepath)

        except:
            print('Folder path not found')

        logging.debug("unzip_complete(): Complete") 

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
            self.zipLineEdit.setReadOnly(True)
            self.zipLineEdit.setStyleSheet("background-color : grey")
            self.chooseFileButton.setEnabled(False)
            self.chooseFileButton.setStyleSheet("background-color : grey")
            self.import_project_button.setEnabled(False)
            self.import_project_button.setStyleSheet("background-color : grey")

    def on_choosefile_button_clicked(self):
        zip_file = QFileDialog()
        filenames, _ = QFileDialog.getOpenFileNames(zip_file, "Select File")

        if len(filenames) < 0:
            logging.debug("File choose cancelled")
            return

        if len(filenames) > 0:
            self.zip_to_import = filenames[0]
            self.file_name = os.path.basename(self.zip_to_import)
            if(".zip" not in self.zip_to_import):
                QMessageBox.warning(self,
                                "Not a .zip file",
                                "File selected is not a .zip file!",
                                QMessageBox.Ok)            
                return None

            self.file_name = os.path.splitext(self.file_name)[0]
            configname = self.file_name
            working_dir = os.getcwd()
            self.project_data_folder = os.path.join(working_dir, "ProjectData")
            self.new_project_path = os.path.join(self.project_data_folder, configname)
            if os.path.exists(self.new_project_path):
                QMessageBox.warning(self,
                                "Name Exists",
                                "The project name specified and directory already exists",
                                QMessageBox.Ok)            
                return None
            else:
                self.zipLineEdit.setText(self.new_project_path)
                self.project_name.setReadOnly(True)
                self.project_name.setStyleSheet("background-color : grey")
                self.pathLineEdit.setReadOnly(True)
                self.pathLineEdit.setStyleSheet("background-color : grey")
                self.create_project_button.setEnabled(False)
                self.create_project_button.setStyleSheet("background-color : grey")
                self.chooseFolderButton.setEnabled(False)
                self.chooseFolderButton.setStyleSheet("background-color : grey")
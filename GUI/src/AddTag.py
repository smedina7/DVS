from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddTag(object):
    def setupUi(self, AddTag):
        AddTag.setObjectName("AddTag")
        AddTag.resize(253, 115)
        self.Buttons = QtWidgets.QDialogButtonBox(AddTag)
        self.Buttons.setGeometry(QtCore.QRect(30, 71, 211, 41))
        self.Buttons.setOrientation(QtCore.Qt.Horizontal)
        self.Buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Buttons.setObjectName("Buttons")
        self.formLayoutWidget = QtWidgets.QWidget(AddTag)
        self.formLayoutWidget.setGeometry(QtCore.QRect(19, 19, 221, 21))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.retranslateUi(AddTag)
        self.Buttons.accepted.connect(AddTag.accept)
        self.Buttons.rejected.connect(AddTag.reject)
        QtCore.QMetaObject.connectSlotsByName(AddTag)

    def retranslateUi(self, AddTag):
        _translate = QtCore.QCoreApplication.translate
        AddTag.setWindowTitle(_translate("AddTag", "Dialog"))
        self.label.setText(_translate("AddTag", "Add Tag:"))

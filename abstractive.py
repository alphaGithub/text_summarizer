# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abstractive.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from generate_summary import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(703, 298)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 681, 121))
        self.textEdit.setObjectName("textEdit")
        self.buttonSummary = QtWidgets.QPushButton(Form)
        self.buttonSummary.setGeometry(QtCore.QRect(10, 150, 681, 27))
        self.buttonSummary.setObjectName("buttonSummary")
        self.output = QtWidgets.QLabel(Form)
        self.output.setGeometry(QtCore.QRect(20, 200, 661, 61))
        self.output.setObjectName("output")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Text Summerizer"))
        self.buttonSummary.setText(_translate("Form", "Generate Summary"))
        self.output.setText(_translate("Form", "Output :"))
        self.buttonSummary.clicked.connect(lambda : self.result())

    def result(self):
        print("Processing ......")
        text = self.textEdit.toPlainText()
        text = text.strip()
        if text == "":
            self.output.setText("Error :Please Enter Text  above ")
            return 
        
        out = summary(text)
        self.output.setText("Summary :" + out)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())



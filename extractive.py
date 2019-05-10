# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extractive.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import summary
import sys 

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(747, 493)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.label.setObjectName("label")
        self.generate = QtWidgets.QPushButton(Form)
        self.generate.setGeometry(QtCore.QRect(10, 230, 141, 27))
        self.generate.setObjectName("generate")
        self.text_input = QtWidgets.QTextEdit(Form)
        self.text_input.setGeometry(QtCore.QRect(10, 30, 721, 191))
        self.text_input.setReadOnly(False)
        self.text_input.setObjectName("text_input")
        self.textOut = QtWidgets.QTextEdit(Form)
        self.textOut.setGeometry(QtCore.QRect(10, 270, 721, 181))
        self.textOut.setReadOnly(True)
        self.textOut.setObjectName("textOut")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Text Summarizer"))
        self.label.setText(_translate("Form", "Enter the Text :"))
        self.generate.setText(_translate("Form", "Generate Summary"))
        self.generate.clicked.connect(lambda : self.summary())

    def summary(self):
        text = self.text_input.toPlainText()
        s = summary.gen_summary(text)
        self.textOut.setText(s)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cart_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(682, 433)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 370, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 30, 681, 334))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spinBox_4 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_4.setObjectName("spinBox_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinBox_4)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.spinBox_5 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_5.setObjectName("spinBox_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBox_5)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spinBox_6 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_6.setObjectName("spinBox_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBox_6)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.spinBox_7 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_7.setObjectName("spinBox_7")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.spinBox_7)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.spinBox_8 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_8.setObjectName("spinBox_8")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spinBox_8)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.label_9)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Carrello"))
        self.label.setText(_translate("Dialog", "Latte 🍼"))
        self.label_2.setText(_translate("Dialog", "Mela 🍎 "))
        self.label_3.setText(_translate("Dialog", "Carne 🍖"))
        self.label_4.setText(_translate("Dialog", "Pasta 🍝 "))
        self.label_5.setText(_translate("Dialog", "Cereali 🥣"))
        self.label_6.setText(_translate("Dialog", "Uova 🥚"))
        self.label_7.setText(_translate("Dialog", "Formaggio 🧀"))
        self.label_8.setText(_translate("Dialog", "Pane  🥖"))
        self.label_10.setText(_translate("Dialog", "Tempo trascorso: "))
        self.label_9.setText(_translate("Dialog", "0 secondi"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

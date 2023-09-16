# Form implementation generated from reading ui file 'dialog_FilenameThing.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import logging

from PyQt6 import QtCore, QtGui, QtWidgets

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Popup(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 406)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.userIDLabel = QtWidgets.QLabel(parent=Dialog)
        self.userIDLabel.setObjectName("userIDLabel")
        self.verticalLayout.addWidget(self.userIDLabel)
        self.userIDLine = QtWidgets.QLineEdit(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userIDLine.sizePolicy().hasHeightForWidth())
        self.userIDLine.setSizePolicy(sizePolicy)
        self.userIDLine.setObjectName("userIDLine")
        self.verticalLayout.addWidget(self.userIDLine)
        self.customFileLabel = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customFileLabel.sizePolicy().hasHeightForWidth())
        self.customFileLabel.setSizePolicy(sizePolicy)
        self.customFileLabel.setObjectName("customFileLabel")
        self.verticalLayout.addWidget(self.customFileLabel)
        self.customFileLine = QtWidgets.QLineEdit(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customFileLine.sizePolicy().hasHeightForWidth())
        self.customFileLine.setSizePolicy(sizePolicy)
        self.customFileLine.setObjectName("customFileLine")
        self.verticalLayout.addWidget(self.customFileLine)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelA = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelA.sizePolicy().hasHeightForWidth())
        self.labelA.setSizePolicy(sizePolicy)
        self.labelA.setObjectName("labelA")
        self.gridLayout_3.addWidget(self.labelA, 0, 1, 1, 1)
        self.checkA = QtWidgets.QCheckBox(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkA.sizePolicy().hasHeightForWidth())
        self.checkA.setSizePolicy(sizePolicy)
        self.checkA.setText("")
        self.checkA.setObjectName("checkA")
        self.gridLayout_3.addWidget(self.checkA, 1, 1, 1, 1)
        self.labelC = QtWidgets.QLabel(parent=self.groupBox)
        self.labelC.setObjectName("labelC")
        self.gridLayout_3.addWidget(self.labelC, 0, 3, 1, 1)
        self.labelD = QtWidgets.QLabel(parent=self.groupBox)
        self.labelD.setObjectName("labelD")
        self.gridLayout_3.addWidget(self.labelD, 0, 4, 1, 1)
        self.labelB = QtWidgets.QLabel(parent=self.groupBox)
        self.labelB.setObjectName("labelB")
        self.gridLayout_3.addWidget(self.labelB, 0, 2, 1, 1)
        self.vLeadsLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vLeadsLabel.sizePolicy().hasHeightForWidth())
        self.vLeadsLabel.setSizePolicy(sizePolicy)
        self.vLeadsLabel.setObjectName("vLeadsLabel")
        self.gridLayout_3.addWidget(self.vLeadsLabel, 1, 0, 1, 1)
        self.checkB = QtWidgets.QCheckBox(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkB.sizePolicy().hasHeightForWidth())
        self.checkB.setSizePolicy(sizePolicy)
        self.checkB.setText("")
        self.checkB.setObjectName("checkB")
        self.gridLayout_3.addWidget(self.checkB, 1, 2, 1, 1)
        self.checkC = QtWidgets.QCheckBox(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkC.sizePolicy().hasHeightForWidth())
        self.checkC.setSizePolicy(sizePolicy)
        self.checkC.setText("")
        self.checkC.setObjectName("checkC")
        self.gridLayout_3.addWidget(self.checkC, 1, 3, 1, 1)
        self.checkD = QtWidgets.QCheckBox(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkD.sizePolicy().hasHeightForWidth())
        self.checkD.setSizePolicy(sizePolicy)
        self.checkD.setText("")
        self.checkD.setObjectName("checkD")
        self.gridLayout_3.addWidget(self.checkD, 1, 4, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_5.addItem(spacerItem)
        self.customSampleLabel = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customSampleLabel.sizePolicy().hasHeightForWidth())
        self.customSampleLabel.setSizePolicy(sizePolicy)
        self.customSampleLabel.setObjectName("customSampleLabel")
        self.verticalLayout_5.addWidget(self.customSampleLabel)
        self.customSampleLine = QtWidgets.QLineEdit(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customSampleLine.sizePolicy().hasHeightForWidth())
        self.customSampleLine.setSizePolicy(sizePolicy)
        self.customSampleLine.setObjectName("customSampleLine")
        self.verticalLayout_5.addWidget(self.customSampleLine)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(1, 3, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_6.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.warming_coolingCombo = QtWidgets.QComboBox(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warming_coolingCombo.sizePolicy().hasHeightForWidth())
        self.warming_coolingCombo.setSizePolicy(sizePolicy)
        self.warming_coolingCombo.setObjectName("warming_coolingCombo")
        self.warming_coolingCombo.addItem("")
        self.warming_coolingCombo.addItem("")
        self.warming_coolingCombo.addItem("")
        self.warming_coolingCombo.addItem("")
        self.verticalLayout_6.addWidget(self.warming_coolingCombo)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.referenceTempLabel = QtWidgets.QLabel(parent=Dialog)
        self.referenceTempLabel.setObjectName("referenceTempLabel")
        self.gridLayout.addWidget(self.referenceTempLabel, 3, 1, 1, 1)
        self.rubyFrequencyLine = QtWidgets.QLineEdit(parent=Dialog)
        self.rubyFrequencyLine.setObjectName("rubyFrequencyLine")
        self.gridLayout.addWidget(self.rubyFrequencyLine, 2, 0, 1, 1)
        self.referenceTempLine = QtWidgets.QLineEdit(parent=Dialog)
        self.referenceTempLine.setObjectName("referenceTempLine")
        self.gridLayout.addWidget(self.referenceTempLine, 4, 1, 1, 1)
        self.referenceFrequencyLine = QtWidgets.QLineEdit(parent=Dialog)
        self.referenceFrequencyLine.setObjectName("referenceFrequencyLine")
        self.gridLayout.addWidget(self.referenceFrequencyLine, 4, 0, 1, 1)
        self.referenceFrequencyLabel = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.referenceFrequencyLabel.sizePolicy().hasHeightForWidth())
        self.referenceFrequencyLabel.setSizePolicy(sizePolicy)
        self.referenceFrequencyLabel.setObjectName("referenceFrequencyLabel")
        self.gridLayout.addWidget(self.referenceFrequencyLabel, 3, 0, 1, 1)
        self.temperatureLabel = QtWidgets.QLabel(parent=Dialog)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.gridLayout.addWidget(self.temperatureLabel, 1, 1, 1, 1)
        self.rubyFrequencyLabel = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rubyFrequencyLabel.sizePolicy().hasHeightForWidth())
        self.rubyFrequencyLabel.setSizePolicy(sizePolicy)
        self.rubyFrequencyLabel.setObjectName("rubyFrequencyLabel")
        self.gridLayout.addWidget(self.rubyFrequencyLabel, 1, 0, 1, 1)
        self.temperatureLine = QtWidgets.QLineEdit(parent=Dialog)
        self.temperatureLine.setObjectName("temperatureLine")
        self.gridLayout.addWidget(self.temperatureLine, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.userIDLabel.setText(_translate("Dialog", "User ID:"))
        self.customFileLabel.setText(_translate("Dialog", "Custom Filename:"))
        self.labelA.setText(_translate("Dialog", "A"))
        self.labelC.setText(_translate("Dialog", "C"))
        self.labelD.setText(_translate("Dialog", "D"))
        self.labelB.setText(_translate("Dialog", "B"))
        self.vLeadsLabel.setText(_translate("Dialog", "V Leads:"))
        self.customSampleLabel.setText(_translate("Dialog", "Sample Name:"))
        self.label.setText(_translate("Dialog", "Type:"))
        self.warming_coolingCombo.setItemText(0, _translate("Dialog", "Warming"))
        self.warming_coolingCombo.setItemText(1, _translate("Dialog", "Cooling"))
        self.warming_coolingCombo.setItemText(2, _translate("Dialog", "Test"))
        self.warming_coolingCombo.setItemText(3, _translate("Dialog", "N/A"))
        self.referenceTempLabel.setText(_translate("Dialog", "Reference Temp (Optional):"))
        self.referenceFrequencyLabel.setText(_translate("Dialog", "Reference Frequency:"))
        self.temperatureLabel.setText(_translate("Dialog", "Temperature (Optional):"))
        self.rubyFrequencyLabel.setText(_translate("Dialog", "Ruby Frequency:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Popup()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
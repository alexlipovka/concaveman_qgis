# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\aWork\coding\qgis-plugs-dev\concaveman_qgis\concaveman_qgis_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConcavemanQGISDialogBase(object):
    def setupUi(self, ConcavemanQGISDialogBase):
        ConcavemanQGISDialogBase.setObjectName("ConcavemanQGISDialogBase")
        ConcavemanQGISDialogBase.resize(401, 168)
        self.button_box = QtWidgets.QDialogButtonBox(ConcavemanQGISDialogBase)
        self.button_box.setGeometry(QtCore.QRect(40, 120, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.layoutWidget = QtWidgets.QWidget(ConcavemanQGISDialogBase)
        self.layoutWidget.setGeometry(QtCore.QRect(18, 70, 361, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dsbConcavity = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.dsbConcavity.setSingleStep(0.1)
        self.dsbConcavity.setObjectName("dsbConcavity")
        self.horizontalLayout_2.addWidget(self.dsbConcavity)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.dsbLenThres = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.dsbLenThres.setDecimals(4)
        self.dsbLenThres.setSingleStep(0.001)
        self.dsbLenThres.setObjectName("dsbLenThres")
        self.horizontalLayout.addWidget(self.dsbLenThres)
        self.chkSelected = QtWidgets.QCheckBox(ConcavemanQGISDialogBase)
        self.chkSelected.setGeometry(QtCore.QRect(280, 20, 111, 17))
        self.chkSelected.setObjectName("chkSelected")
        self.mPointLayers = QgsMapLayerComboBox(ConcavemanQGISDialogBase)
        self.mPointLayers.setGeometry(QtCore.QRect(20, 10, 251, 27))
        self.mPointLayers.setShowCrs(True)
        self.mPointLayers.setObjectName("mPointLayers")
        self.chkConvex = QtWidgets.QCheckBox(ConcavemanQGISDialogBase)
        self.chkConvex.setGeometry(QtCore.QRect(20, 130, 151, 17))
        self.chkConvex.setObjectName("chkConvex")

        self.retranslateUi(ConcavemanQGISDialogBase)
        self.button_box.accepted.connect(ConcavemanQGISDialogBase.accept)
        self.button_box.rejected.connect(ConcavemanQGISDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ConcavemanQGISDialogBase)

    def retranslateUi(self, ConcavemanQGISDialogBase):
        _translate = QtCore.QCoreApplication.translate
        ConcavemanQGISDialogBase.setWindowTitle(_translate("ConcavemanQGISDialogBase", "Concaveman QGIS"))
        self.label_2.setText(_translate("ConcavemanQGISDialogBase", "Concavity:"))
        self.label_3.setText(_translate("ConcavemanQGISDialogBase", "Length threshold:"))
        self.chkSelected.setText(_translate("ConcavemanQGISDialogBase", "Selected features"))
        self.chkConvex.setText(_translate("ConcavemanQGISDialogBase", "Make Convex Hull"))
from qgsmaplayercombobox import QgsMapLayerComboBox

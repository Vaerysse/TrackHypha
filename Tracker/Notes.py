# -*- coding: utf-8 -*-

# =============================================================================
#     This module is part of TrackHypha, an application that analyzes the 
#     filamentous network of a mushroom by following one of its apex. 
#     Copyright (C)  2019  Salomé Attar, 
#                          Bouthayna Haltout, 
#                          Sébastien Maillos, 
#                          Laura Xénard
# 
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program. If not, see https://www.gnu.org/licenses/.
# =============================================================================


"""
:Synopsis: 
     This module defines the export window, it creates the main visuals of the export window. It has only one class:
         
         * Ui_Dialog
   
.. moduleauthor:: Haltout Bouthayna
"""


from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    """
    Main class initializing the export window of the project. 
    
    .. codeauthor:: Bouthayna Haltout
    """
    
    def setupUi(self, Dialog):
        """
        Class constructor.
        
        :param Dialog: the dialog to setup
        :type Dialog: PyQt5.QtWidgets.QDialog
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(497, 385)
        Dialog.resize(477, 344)
        self.data = QtWidgets.QCheckBox(Dialog)
        self.data.setGeometry(QtCore.QRect(30, 190, 87, 20))
        self.data.setObjectName("Data.txt") # CheckBox for the text data.
#        self.data.setChecked(True) 
        self.fImg = QtWidgets.QCheckBox(Dialog)
        self.fImg.setGeometry(QtCore.QRect(150, 190, 101, 20))
        self.fImg.setObjectName("Final image") # CheckBox for the final image data.
#        self.fImg.setChecked(True) 
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 160, 181, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 10, 211, 16))
        self.label_2.setObjectName("label_2")
        self.sImg = QtWidgets.QCheckBox(Dialog) # CheckBox for the steps image data.
        self.sImg.setGeometry(QtCore.QRect(290, 190, 111, 20))
        self.sImg.setObjectName("Step Images")
        self.sImg.setChecked(False) 
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(280, 280, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(40, 40, 391, 111))
        self.textEdit.setObjectName("textEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 230, 421, 41))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        """
        Function initializing the names of the check boxes and labels.
        
        :param Dialog: the dialog to retranslate
        :type Dialog: PyQt5.QtWidgets.QDialog        
    
        .. codeauthor:: Bouthayna Haltout
        """
        # Sets the names.
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Form", "Export"))
        self.data.setText(_translate("Form", "Data.txt  "))
        self.fImg.setText(_translate("Form", "Final image "))
        self.label.setText(_translate("Form", "Options Export :"))
        self.label_2.setText(_translate("Form", "Enter your notes for the export :"))
        self.sImg.setText(_translate("Form", "Steps images"))
        self.label_3.setText(_translate("Form", "Warning : Exporting the steps images may take some time and a lot of disk space.  "))
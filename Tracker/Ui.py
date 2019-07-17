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
    This module defines the mainwindow, it creates the main visuals of the mainwindow. It has only one class:
        
        * Ui_MainWindow
    
.. moduleauthor:: Haltout Bouthayna
"""


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QAction
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    """
    Main class initializing the MainWindow of the project. 
    
    .. codeauthor:: Bouthayna Haltout
    """
    
    def setupUi(self, MainWindow):
        """
        Class constructor.
        
        :param MainWindow MainWindow: the main window in which to create the buttons
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        MainWindow.setObjectName("TrackHypha")# Name of the application and of the window.
        MainWindow.resize(1000, 708)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
          
        ## Window settings ##
        
        self.screenSize = QDesktopWidget().screenGeometry(-1) # -1 to get the main screen.
        self.padding = 100 # to center the window in the screen and the image in the QLabel.
        self.left = 0 + self.padding
        self.top = 0 + self.padding
        self.width = self.screenSize.width() - self.padding*2
        self.height = self.screenSize.height() - self.padding*2
        
        ## Creation of the menu bar ##
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuNew = QtWidgets.QMenu(self.menubar)
        self.menuNew.setObjectName("menuNew")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #Creation  New, Open, Save, export and close in File.
        
        self.actionNew = QtWidgets.QAction(MainWindow, shortcut="Ctrl+N")
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow, shortcut="Ctrl+O")
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow, shortcut="Ctrl+S")
        self.actionSave.setObjectName("actionSave")
        self.actionExport = QtWidgets.QAction(MainWindow, shortcut="Ctrl+E")
        self.actionExport.setObjectName("actionExport")
        self.actionClose = QtWidgets.QAction(MainWindow, shortcut="Ctrl+C")
        self.actionExport.setObjectName("actionClose")
        
        self.menuNew.addAction(self.actionNew)
        self.menuNew.addAction(self.actionOpen)
        self.menuNew.addAction(self.actionSave)
        self.menuNew.addAction(self.actionExport)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionClose)
        self.menubar.addAction(self.menuNew.menuAction())
        

        self.retranslateUi(MainWindow)
        
        self.playAction = QAction(QIcon("icons/play.png"),"Run ",MainWindow)
        self.playAction.setShortcut("Ctrl+P")
        self.playAction.setStatusTip("Run the analysis.")
        self.fitToWindowAction = QAction(QIcon("icons/fittowindow.png"),"fitToWindow ",MainWindow)
        self.fitToWindowAction.setStatusTip("Fit the image to the window")
        self.fitToWindowAction.setShortcut("Ctrl+W")
        self.zoominAction = QAction(QIcon("icons/zoomin.png"),"Zoom-in",MainWindow)
        self.zoominAction.setStatusTip("Zoom in the image")
        self.zoominAction.setShortcut("Ctrl++")
        self.zoomoutAction = QAction(QIcon("icons/zoomout.png"),"Zoom-out",MainWindow)
        self.zoomoutAction.setStatusTip("Zoom out of the image")
        self.zoomoutAction.setShortcut("Ctrl+-")    
        self.truesizeAction = QAction(QIcon("icons/truesize.png"),"True size",MainWindow)
        self.truesizeAction.setStatusTip("Display the image in its true size")
        self.truesizeAction.setShortcut("Ctrl+=")
        self.nextAction = QAction(QIcon("icons/next.png"),"Next Image",MainWindow)
        self.nextAction.setStatusTip("Next image")
        self.nextAction.setShortcut("Ctrl+>")
        self.previousAction = QAction(QIcon("icons/previous.png"),"Previous Image",MainWindow)
        self.previousAction.setStatusTip("Previous image")
        self.previousAction.setShortcut("Ctrl+<")
        self.nextAnalyseAction = QAction(QIcon("icons/next.png"),"Next Step",MainWindow)
        self.nextAnalyseAction.setStatusTip("Next step")
        self.nextAnalyseAction.setShortcut("Ctrl+D")
        self.previousAnalysisAction = QAction(QIcon("icons/previous.png"),"Previous Step",MainWindow)
        self.previousAnalysisAction.setStatusTip("Previous step")
        self.previousAnalysisAction.setShortcut("Ctrl+A")
        
    def retranslateUi(self, MainWindow): 
        """
        Function initializing the names of the menu bar. 
        
        :param MainWindow MainWindow: the main window in which to create the buttons
    
        .. codeauthor:: Bouthayna Haltout
        """
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TrackHypha"))
        self.menuNew.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionClose.setText(_translate("MainWindow", "Close"))




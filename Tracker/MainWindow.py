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

# =============================================================================
#     This sites helped write the code below: 
#    
#    *https://stackoverflow.com/questions/43569167/pyqt5-resize-label-to-fill-the-whole-window
#    *http://zetcode.com/gui/pyqt5/widgets2/
#    *https://github.com/xinntao/HandyViewer/blob/master/HandyViewer.py
# =============================================================================


"""
:Synopsis: 
    This module represents and manages the structure of the Main window seen by the user. 
    This module contains three classes: 
        
        * MouseTracker
        * MainWindow
        * TaskBar
    
    It is the User Interface module of the application: 
    it links itself to the :mod:`Management` module that is linked to all the other modules.

.. moduleauthor:: Haltout Bouthayna
"""
 

import sys

from PyQt5.QtWidgets import (QDialog, QApplication, QMainWindow, QProgressBar, QStatusBar, 
                             QFileDialog, QLabel, QScrollArea, QInputDialog, QMessageBox, QLineEdit)
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import ImageQt

from Notes import Ui_Dialog as Form
import Ui
import Management
import Mushroom


class MouseTracker(QLabel):
    """
    Class adding a mouse position tracker to a QLabel. 
    
    .. codeauthor:: Laura Xénard       
    .. codeauthor:: Bouthayna Haltout   
    """
    
    def __init__(self):
        """
        Class constructor.
        
        .. codeauthor:: Laura Xénard
        """
        
        super().__init__()
        self.setMouseTracking(False) # activates only when an image is displayed
        
    def mouseMoveEvent(self, event):
        """
        Event method that tracks the mouse position in the QLabel and displays it.
        
        :param event: the detected event
        :type event: PyQt5.QtGui.QMouseEvent
        
        .. codeauthor:: Laura Xénard
        """
        
        xImg = int(event.x() / MainWindow.scaleFactor) # Real mouse abscissa position in the image.
        yImg = int(event.y() / MainWindow.scaleFactor) # Real mouse ordinate position in the image.          
        MainWindow.mouseCoordinates.setText('({}, {})'.format(xImg, yImg)) # Display the mouse position in the status bar.
            
    def mousePressEvent(self, event):
        """
        Event method that handle the mouse pressing event.
        
        :param event: the detected event
        :type event: PyQt5.QtGui.QMouseEvent
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        if MainWindow.apexS:# If apexS in MainWindow == True, we look at the mousePressEvent, and get the position of the click in the image.          
            MainWindow.x = int(event.x() / MainWindow.scaleFactor) # Real mouse abscissa position in the image.
            MainWindow.y = int(event.y() / MainWindow.scaleFactor) # Real mouse ordinate position in the image.
            MainWindow.checkApex()# We launch the method checkApex() when the apexS == True. 


class MainWindow(QMainWindow):  
    """
    Main class displaying the MainWindow of the project. 
    
    .. codeauthor:: Bouthayna Haltout
    """
    
    def __init__(self):
        """
        Class constructor.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        super(MainWindow, self).__init__()
        self.MainUi = Ui.Ui_MainWindow()
        self.MainUi.setupUi(self)
        self.setGeometry(self.MainUi.left, self.MainUi.top, self.MainUi.width, self.MainUi.height)
        self.manage = Management.Mana() 
        
        self.scaleFactor = 1.0   
        self.fitScaleFactor = 1.0
        self.x = -1 # Setting x and y to -1, as long as the coordinates of the apex are not chosen. 
        self.y = -1
        self.apexS = False # We set it to false to desactivate the choice of the apex.

   
        # Connecting the menu items to their respective functions.
        self.MainUi.actionNew.triggered.connect(self.new)
        self.MainUi.actionSave.triggered.connect(self.save)
        self.MainUi.actionOpen.triggered.connect(self.open)
        self.MainUi.actionExport.triggered.connect(self.export)
        self.MainUi.actionClose.triggered.connect(self.close)
 
        ## Connecting each action of the Toolbar to the its function ##
     
        # We connect the icons to the assigned functions.
        self.MainUi.playAction.triggered.connect(self.play)       
        self.MainUi.fitToWindowAction.triggered.connect(self.scaleToFit)       
        self.MainUi.zoominAction.triggered.connect(self.zoomIn)       
        self.MainUi.zoomoutAction.triggered.connect(self.zoomOut)       
        self.MainUi.truesizeAction.triggered.connect(self.trueSize)       
        self.MainUi.nextAction.triggered.connect(self.nextImg)       
        self.MainUi.previousAction.triggered.connect(self.previousImg)
        self.MainUi.nextAnalyseAction.triggered.connect(self.nextAnalysisImg)       
        self.MainUi.previousAnalysisAction.triggered.connect(self.previousAnalysisImg)
        
        # titleAfterAnalysis and titleBeforeAnalysis showing the total number of images before and after the analysis.   
        titleAfterAnalysis = QLabel("Steps Navigation")#ou analysis
        titleBeforeAnalysis = QLabel("Images Navigation") 
        self.totalNumberOfImg = QLabel(" / 0") 
        self.totalNumberOfStep = QLabel(" / 0")
        
        # Connecting the QLineEdit to the pushOk functions allowing the user to go to the desired image.
        self.numberImg = QLineEdit(self)
        self.numberImg.setFixedWidth(25)
        self.numberImg.returnPressed.connect(self.pushOkImg)
        self.numberStep = QLineEdit(self)
        self.numberStep.setFixedWidth(25)
        self.numberStep.returnPressed.connect(self.pushOkStep)
        
        # Creating and connecting a QprogressBar that will allow the user to know that the analysis is running.
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
 
        # Creating the toolBar and adding all the widgets to it.
        self.toolbar = self.addToolBar("Options")
        self.toolbar.addWidget(titleBeforeAnalysis)      
        self.toolbar.addAction(self.MainUi.previousAction)
        self.toolbar.addWidget(self.numberImg)
        self.toolbar.addWidget(self.totalNumberOfImg)
        self.toolbar.addAction(self.MainUi.nextAction)         
        self.toolbar.addSeparator()      
        self.toolbar.addAction(self.MainUi.playAction)       
        self.toolbar.addAction(self.MainUi.fitToWindowAction)
        self.toolbar.addAction(self.MainUi.zoomoutAction)
        self.toolbar.addAction(self.MainUi.truesizeAction)
        self.toolbar.addAction(self.MainUi.zoominAction)             
        self.toolbar.addSeparator()       
        self.toolbar.addWidget(titleAfterAnalysis)
        self.toolbar.addAction(self.MainUi.previousAnalysisAction)
        self.toolbar.addWidget(self.numberStep)        
        self.toolbar.addWidget(self.totalNumberOfStep)
        self.toolbar.addAction(self.MainUi.nextAnalyseAction)       
        self.toolbar.addSeparator()       
        self.toolbar.addWidget(self.progressBar)         
        self.addToolBarBreak()
        
        ## Image area and scroll area ##
        
        self.imageLabel = MouseTracker()
        self.imageLabel.resize(self.MainUi.width-self.MainUi.padding, self.MainUi.height-self.MainUi.padding)
        
        # Sets the scroll area where the images are going to be opened. 
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)
        
        # Setting the Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusMessage = QLabel('Please create or open a project.')
        self.statusBar.addWidget(self.statusMessage, 1)        
        self.mouseCoordinates = QLabel()
        self.statusBar.addWidget(self.mouseCoordinates, 0)
        
        # Connecting the progressBar to the function confirm that will update the Value
        self.myLongTask = TaskBar()
        self.myLongTask.taskFinished.connect(self.confirm)
        
    ## Project methods ## 
       
    def new(self):
        """ 
        Initializes path as a path directory and sends it to the :mod:`Management` module that then gets the set of data in the directory. 
        It then displays the GreyImages returned by the :mod:`Management` module. And sets the statusBar and the total number of steps and images of the project.  
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        path = str(QFileDialog.getExistingDirectory(self, "Directory Selection")) # Get the path directory as a string.
        if path != "":
            boole, message = self.manage.new_project(path) # Sends the path to Management.
            if boole == True:
                self.scaleFactor = 1.0
                self.fitScaleFactor = 1.0
                self.imageLabel = MouseTracker()
                self.imageLabel.resize(self.MainUi.width-self.MainUi.padding, self.MainUi.height-self.MainUi.padding)
                self.imageLabel.setMouseTracking(True) # activates the mouse position tracking on the image.       
                self.scrollArea.setWidget(self.imageLabel)
                self.displayImgGrey()
                self.statusMessage.setText("Select the parameters for the analysis.")
                self.fitToWindow()
                self.totalNumberOfStep.setText(" / 0")
                self.totalNumberOfImg.setText(" / {}".format(len(self.manage.project.greyPics)))# Sets the total number of images before the analysis.
            else:
                QMessageBox.critical(self, "Error", message, QMessageBox.Ok)
  
    def open(self):
        """ 
        Initializes the fileName as the file name of the path of a pre-existing project, that the user wants to open. It then sends it to :mod:`Management` module.
        After that, it displays the redImages, sets the satusBar and the total number of steps and images of the project.  
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        fileName, _ = QFileDialog.getOpenFileName(self, "Project Selection","","All Files (*)") # Get the name of the file to open.
        if fileName != "":
            boole, message = self.manage.load_project(fileName) # Sends the fileName to Management.
            if boole == True:
                self.scaleFactor = 1.0
                self.fitScaleFactor = 1.0
                self.imageLabel = MouseTracker()
                self.imageLabel.resize(self.MainUi.width-self.MainUi.padding, self.MainUi.height-self.MainUi.padding)            
                self.imageLabel.setMouseTracking(True) # activate the mouse position tracking on the image        
                self.scrollArea.setWidget(self.imageLabel)
                self.displayImgRed()
                self.statusMessage.setText("")
                self.fitToWindow()
                self.totalNumberOfStep.setText(" / {}".format(len(self.manage.project.analysis.steps)))
                self.totalNumberOfImg.setText(" / {}".format(len(self.manage.project.greyPics)))
            else:
                QMessageBox.critical(self, "Error", message, QMessageBox.Ok)
      
    def zoomIn(self):
        """
        Zooms in the image of 15%.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.scaleImage(1.15)
    
    def zoomOut(self):
        """
        Zooms out the image of 15%.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.scaleImage(0.85)
    
    def trueSize(self):
        """
        Re-scales the image to its true size.
        
        .. codeauthor:: Laura Xénard
        """
        
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
    
    def fitToWindow(self): 
        """
        Scales the image to fit the window.
        
        .. codeauthor:: Laura Xénard
        """
        
        if (self.pixmap.height() > self.imageLabel.height()) or (self.pixmap.width() > self.imageLabel.width()):
            if self.imageLabel.height() <= self.imageLabel.width():
                label_height_resized = self.imageLabel.height()
                label_width_resized = self.pixmap.width() * self.imageLabel.height() / self.pixmap.height()
            else:
                label_height_resized = self.pixmap.height() * self.imageLabel.width() / self.pixmap.width()
                label_width_resized = self.imageLabel.width()
        else:
            label_width_resized = self.pixmap.width()
            label_height_resized = self.pixmap.height()
         
        self.imageLabel.resize(label_width_resized, label_height_resized)
        self.imageLabel.setScaledContents(True)
        self.computeFitToWindowScaleFactor()   
    
    def scaleToFit(self):
        """
        Scales the image to fit the window.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.scaleFactor = self.fitScaleFactor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), self.fitScaleFactor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), self.fitScaleFactor)
    
    def scaleImage(self, factor):
        """
        Scales the image.
        
        :param float factor: the zoom factor
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
    
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
    
    def computeFitToWindowScaleFactor(self):
        """
        Computes the scale factor needed to fit an image to the window.
        
        .. codeauthor:: Laura Xénard
        """
        
        widthScaleFactor = self.imageLabel.width() / self.pixmap.width() 
        heightScaleFactor = self.imageLabel.height() / self.pixmap.height() 
        self.scaleFactor =  (widthScaleFactor + heightScaleFactor) / 2
        self.fitScaleFactor = self.scaleFactor
    
    def adjustScrollBar(self, scrollBar, factor):
        """
        Adjusts the scroll bar.
        
        :param scrollBar: the scrollbar to adjust
        :type scrollBar: PyQt5.QtWidgets.QScrollBar
        :param float factor: the zoom factor
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep()/2)))
        
    
    ## Pre-analysis methods ##
    
    def displayImgGrey(self):
        """
        Displays the grey Images before an analysis, given by the module :mod:`Management`.
        
        .. codeauthor:: Bouthayna Haltout
        """

        current = self.manage.project.currentImg # Get the current image from Management.
        image = self.manage.project.greyPics[current][0] # Displays the current image. 
        qimg = ImageQt.ImageQt(image)
        self.pixmap = QPixmap.fromImage(qimg)
        self.numberImg.setText(str(self.manage.project.currentImg+1))
        isdisplayed = self.imageLabel.setPixmap(self.pixmap) 
        if isdisplayed == False: # If the image does not display, it goes back to the previous image displayed.
            self.manage.project.greyImgNotDisplayed 
            image = self.manage.project.greyPics[current][0] 
    
    def nextImg(self):
        """
        Allows the user to go to the next non-analyzed image.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.manage.next_img()
        self.displayImgGrey()
        
    def previousImg(self):
        """
        Allows the user to go to the previous non-analyzed image.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.manage.previous_img()      
        self.displayImgGrey()

    def pushOkImg(self):
        """
        Allows the user to go to the non-analyzed image of their choice.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        inputNumber= self.numberImg.text()
        if inputNumber.isdigit():
            info = "You selected `{0}`." 
        else:
            info = "Please select a number, `{0}` isn't valid."
            QMessageBox.about(self,'Error', info.format(inputNumber))
        
        i = self.manage.go_to_img(int(inputNumber)-1)
        
        if i == 0: 
            self.displayImgGrey()
        else: 
            QMessageBox.about(self, 'Error', "The number typed is not a valid number.")
         
    
    def play(self):
        """
        Allows the user to start initializing the parameters for the analysis.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.manage.clear()
        self.apexS = True # We set apexS to true as a condition 
        selectApex = QMessageBox.question(self, 'Apex Selection', "You can select an apex on this image, would you like to continue?", QMessageBox.Yes, QMessageBox.No)
        if selectApex == QMessageBox.No: # The click is always detected, as soon as apexS is == True, the coordinates of click are saved.
            self.apexS = False

    def checkApex(self):
        isApex, realCoord = self.manage.check_apex(Mushroom.Coordinates(self.x, self.y))
        if isApex:
            selectApex = QMessageBox.question(self, 'Apex Selection', "You have selected an apex on this image. Do you want to keep this apex for the analysis?", QMessageBox.Yes, QMessageBox.No)
            if selectApex == QMessageBox.Yes:
                self.manage.select_apex(realCoord)
                self.PopUp()	
                self.apexS= False # Once the apex is selected we put back apexS to false to not save the coordinates anymore. 
            else:
                self.apexS = False
                self.progressBar.setValue(0)
        else:
            QMessageBox.question(self, 'Apex Selection', "This is not an apex. Please select an apex to run an analysis.", QMessageBox.Retry)          
    
    def PopUp(self):
        endImg, ok = QInputDialog.getInt(self, 'Last Image Selection', 
            'Enter the last image for the analysis:',
            len(self.manage.project.greyPics),self.manage.project.currentImg+1,len(self.manage.project.greyPics)) # We put the length of the images as the default number and the maximum, current image +1 as the minimum. 

        if ok:     
            
            if int(endImg):
                info = "You selected `{}`."
                self.manage.select_endImg(endImg-1)
                self.confirm()
                
            else:
                info = "Please select a number, `{}` isn't valid."
                QMessageBox.question(self, 'Error', info.format(endImg), QMessageBox.Retry)

    def confirm(self):
        """
        Allows the user to confirm the parameters selected and to start the analysis.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        confirm = QMessageBox.question(self,'',
                                       "You have selected the apex of coordinates {} from the image {} and have selected as an end image: {}. Click yes to run the analysis.".format(self.manage.project.analysis.startApex,
                                        self.manage.project.analysis.startImg+1, self.manage.project.analysis.endImg+1 ), QMessageBox.Yes, QMessageBox.No)          
        if confirm == QMessageBox.Yes:
            self.apexS = False
            self.statusMessage.setText("Analysing...")
            self.progressBar.setValue(50)
            message, boolean = self.manage.run()             
            self.totalNumberOfStep.setText(" / {}".format(len(self.manage.project.analysis.steps)))
            if boolean == True :  
                self.progressBar.setValue(100) # The progress bar is at the max when the analysis is done.         
                self.statusMessage.setText(message)
                self.displayImgRed()
            else :
                QMessageBox.information(self," ",message, QMessageBox.Ok)
                self.apexS = False
                self.progressBar.setValue(0)  
        
    ## Post-analysis methods ##
    
    def displayImgRed(self):
        """
        Displays the analyzed images (colorized) after the analysis, given by the :mod:`Management` module.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        if self.manage.project.analysis != None:
            if self.manage.project.analysis.currentStep == 0:
                image = self.manage.project.analysis.finalImg
            else:
                image = self.manage.project.analysis.stepImg
            qimg = ImageQt.ImageQt(image)
            self.pixmap = QPixmap.fromImage(qimg)    
            self.numberStep.setText(str(self.manage.project.analysis.currentStep))
            isdisplayed = self.imageLabel.setPixmap(self.pixmap)        
            if isdisplayed == False:
                self.manage.project.colorImgNotDisplayed 
                image = self.manage.project.analysis.stepImg
            
    def pushOkStep(self):
        """
        Allows the user to go to the analyzed image of their choice.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        inputNumber = self.numberStep.text()
        if inputNumber.isdigit():
            info = "You selected `{0}`"
        else:
            info = "Please select a number, `{0}` isn't valid."
            QMessageBox.about(self, 'Error', info.format(inputNumber))
        
        i = self.manage.go_to_step(int(inputNumber))
        
        if i == 0: 
            self.displayImgRed()
        else: 
            QMessageBox.about(self, 'Error', "The number typed is not a valid number.")

    def nextAnalysisImg (self):
        """
        Allows the user to go to the next analyzed image.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.manage.next_step()
        self.displayImgRed()
        
    def previousAnalysisImg (self):
        """
        Allows the user to go to the previous analyzed image.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        self.manage.previous_step()
        self.displayImgRed()
    
    def save(self):
        """ 
        Asks :mod:`Management` to save the current :class:`Project`.
        
        .. codeauthor:: Bouthayna Haltout
        """
        
        message = self.manage.save_project()
        QMessageBox.information(self, " ", message, QMessageBox.Ok) # Shows the message sent by management from the save.
        
    def export(self):
        """ 
        Asks :mod:`Management` to export the data obtained during the analysis of the current :class:`Project`.
        
        :raise AttributeError: if no :class:`Project` attribute has been created

        .. codeauthor:: Bouthayna Haltout
        """
        
        try:
            if self.manage.project.analysis != None:
                dialog = QDialog()
                dialog.ui = Form()
                dialog.ui.setupUi(dialog)
                dialog.exec_()
                dialog.show() # Shows the Notes.py as a QDialog.
                notes = dialog.ui.textEdit.toPlainText() # Retreives the text as notes.
    
                if dialog.ui.data.isChecked() == True: # If data.txt is checked, we initialize textOk to true.
                    self.textOk = True
                else:
                    self.textOk = False   
                    
                if dialog.ui.sImg.isChecked() == True: # If steps images is checked, we initialize imgstepsOk to true.
                    self.imgstepsOk = True
                else:
                    self.imgstepsOk = False 
                    
                if dialog.ui.fImg.isChecked() == True: # If final image is checked, we initialize imgOk to true.
                    self.imgOk = True
                else:
                    self.imgOk = False      
                
                message = self.manage.export_project(notes, self.textOk, self.imgOk, self.imgstepsOk) # Sends the information to Management.
                QMessageBox.information(self, " ", message, QMessageBox.Ok)
            
            else:
                message = "Please run an analysis before trying to export it."
                QMessageBox.warning(self, "Warning", message, QMessageBox.Ok)
        
        except AttributeError:
            message = "Please create or open a project and run an analysis before trying to export it."
            QMessageBox.warning(self, "Warning", message, QMessageBox.Ok)
        
    def closeEvent(self, event):
        """
        Dialog for closing the app, with options on how to proceed - Cancel, Close.
        
        :param event: the detected event
        :type event: PyQt5.QtGui.QCloseEvent 
        """
        
        close = QMessageBox.warning(
            self, "Quit", "Do you want to quit? Any unsaved work will be lost.", QMessageBox.Cancel | QMessageBox.Close)
        if close == QMessageBox.Close:
            self.manage.close() # We clear everything before quitting. 
            app.quit()           
        if close == QMessageBox.Cancel:
            event.ignore()


class TaskBar(QThread):
    """
    Thread class allowing the pyqt signal between the progress bar and the end of the analysis. 
   
    .. codeauthor:: Bouthayna Haltout   
    """
    
    taskFinished = pyqtSignal()# We declare taskFinished as a Signal.
    
    def run(self):
        """
        Emits a signal as soon as it's called.
        """      
        
        self.taskFinished.emit() 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
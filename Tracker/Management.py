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
    This module comprises a unique class, identically named. 
    It is the managing module of the application: it links all the other modules together.

.. moduleauthor:: Sébastien Maillos
.. moduleauthor:: Laura Xénard
"""


from PIL import ImageDraw

import Mushroom as msh
import InOut
import AI


class Mana:
    """ 
    Class managing the calls to all the functionnalities of the application.
        
    :param Project project: the project created by the user
        
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Laura Xénard
    """    
    
    ## Project management methods ##
    
    def new_project(self, path):
        """ 
        Initializes the :class:`Project` attribute of :mod:`Management` from the path obtained by the :mod:`Ui` module 
        by filling the images lists *skelPics* and *greyPics* and loading those images.
        
        :param str path: the path to the project environment given by the user
        :return: a tuple of a boolean and a string indicating the success or failure of the project creation 
        :rtype: (bool, str)
        
        .. codeauthor:: Laura Xénard
        """
        
        self.project = msh.Project(path) # updates the 'project' attribute of 'Management'
        return InOut.new_environment(self.project)
                              
    def load_project(self, path):
        """ 
        Initializes the :class:`Project` attribute of :mod:`Management` from the path of a pre-existing project.
        
        :param str path: the path to the project environment given by the user
        :return: a tuple of a boolean and a string indicating the success or failure of the project creation 
        :rtype: (bool, str)
        
        .. codeauthor:: Laura Xénard
        """
        
        project, loadingOK, message = InOut.open_project(path) # we directly gives the path to InOut which opens the save and extracts the project
        self.project = project # the object 'project'
        return (loadingOK, message)
            
    def save_project(self):
        """ 
        Asks InOut to save the current :class:`Project`.
        
        :return: a string indicating the success or failure of the saving
        :rtype: str
        :raise AttributeError: if no :class:`Project` instance exists
        
        .. codeauthor:: Sébastien Maillos
        """
        
        try:
            message = InOut.save_project(self.project)
        except AttributeError:
            message = "Please create or open a project before trying to save it."
        return message
        
    def export_project(self, notes, txtOk, imgOk, imgstepsOk):
        """ 
        Asks InOut to export the data obtained during the analysis of the current :class:`Project`.

        :param str notes: a string representing the notes written by the user about the current project
        :param bool txtOk: a boolean representing if the text data should be exported
        :param bool imgOk: a boolean representing if the final img should be exported
        :param bool imgstepsOk: a boolean representing if the steps pictures should be exported
        :return: a string indicating the success or failure of the export
        :rtype: str
        
        .. codeauthor:: Sébastien Maillos
        .. codeauthor:: Laura Xénard
        """
        
        self.project.notes = notes # update of the 'notes' attribute of the project
        return InOut.export_project(self.project, txtOk, imgOk, imgstepsOk)    
    

    ## Pre-analysis methods ##
        
    def previous_img(self):
        """
        Asks for the display of the previous image in the list. Slot method for the 'Previous image' button of the interface.
        
        :return: 0 if the image index exists, the non existing index otherwise
        :rtype: int 
        
        .. codeauthor:: Laura Xénard
        """
        
        index = (self.project.currentImg-1) % len(self.project.greyPics)
        return self.go_to_img(index)

    def next_img(self):
        """
        Asks for the display of the next image in the list. Slot method for the 'Next image' button of the interface.
        
        :return: 0 if the image index exists, the non existing index otherwise
        :rtype: int
        
        .. codeauthor:: Laura Xénard
        """
        
        index = (self.project.currentImg+1) % len(self.project.greyPics)
        return self.go_to_img(index)

    def go_to_img(self, index):
        """
        Updates the :class:`Project` information so that the UI module can display a new image. Slot method for the display of a specific image from its index.
        
        :param int index: the index of the image to display
        :return: 0 if the image index exists, the non existing index otherwise
        :rtype: int
        :raise IndexError: if no image exists at the specified index
     
        .. codeauthor:: Laura Xénard
        """
         
        # Check if an image exists at the specified index
        try:
            self.project.greyPics[index][0]
        except IndexError:
            print("WARNING! Index error. No image exists at the index {}".format(index))   
            return(index) # return the inexisting index
            
        self.project.previousImgDisplayed = self.project.currentImg # update of the lastly displayed image
        self.project.currentImg = index # update of the currently displayed image               
        return 0

    
    def greyImgNotDisplayed(self):
        self.project.analysis.currentImg = self.project.analysis.previousImgDisplayed
        
    def check_apex(self, coordSelection):
        """ 
        Asks the AI module to check if the given :class:`Coordinates` in an image is an apex, and update the :class:`Analysis` accordingly.
        
        :param coordSelection: the :class:`Coordinates` given by a user click
        :return: if the given :class:`Coordinates` are those of an apex: True and the real coordinates of the apex. If not: False otherwise and a placeholder :class:`Coordinates`.
        :rtype: (bool, Coordinates)
        
        .. codeauthor:: Sébastien Maillos        
        .. codeauthor:: Laura Xénard
        """

        img = self.project.skelPics[self.project.currentImg]
        isApex, apexRealCoord = AI.is_apex(img, coordSelection)
        if isApex:
            self.project.analysis = msh.Analysis(apexRealCoord, self.project.currentImg) # creation of an object 'Analysis'
            # the image from which the apex is selected is imperatively the start image of the analysis
            return (isApex, apexRealCoord)
        else:
            return (isApex, msh.Coordinates(-1, -1))
    
    def select_apex(self, apexRealCoord):
        """ 
        Updates the :class:`Analysis` with the apex to follow and the start image of the analysis.
        
        :param Coordinates apexRealCoord: the :class:`Coordinates` given by a user click
        :return: a message indicating that the apex and start image have been selected for the analysis
        :rtype: str
        
        .. codeauthor:: Laura Xénard
        """
        
        self.project.analysis = msh.Analysis(apexRealCoord, self.project.currentImg) # creation of an object 'Analysis' isApex
        return "The apex and start image for the analysis have been updated."
    
    def select_endImg(self, endImg):
        """
        Updates the :class:`Analysis` with the end image of the analysis.
        
        :param int endImg: the index of the last image of the analysis, given by the user
        
        .. codeauthor:: Laura Xénard
        """
        
        self.project.analysis.endImg = endImg # update of the last image of the analysis
        return "The end image for the analysis has been updated."
        
        
    ## Analysis methods ##

    def run(self):
        """ 
        Runs an analysis on the list of skeleton images of the project.
        
        :return: a message indicating the state of the analysis
        :rtype: str
        
        .. codeauthor:: Laura Xénard
        """
        
        message, isDone = AI.play_analysis(self.project.skelPics, self.project.analysis)        
        if isDone:
            self.colorize_final_img()
        return (message, isDone)
                  
    def colorize_final_img(self, radius=5, color='red'):
        """
        Colorizes in red all the hyphae explored by the analysis. Works by drawing a red circle on every pixels covered during the analysis. 
        
        :param int radius: the radius of the circle to draw
        :param str color: the color to use for the drawing
            
        .. codeauthor:: Laura Xénard
        """
        
        # Retrieving and copying of the analysis last image
        imgIndex = self.project.analysis.endImg # index of the last image of the analysis
        self.project.analysis.finalImg = self.project.greyPics[imgIndex][0].copy() # copying the img so as to preserve the original img
        
        # Drawing a red circle on every pixel
        draw = ImageDraw.Draw(self.project.analysis.finalImg)
        for index in range(0, len(self.project.analysis.list_pixels), 10):
            coord = self.project.analysis.list_pixels[index]
            draw.ellipse([(coord.x-radius, coord.y-radius), (coord.x+radius, coord.y+radius)], color) # coordinates of the square in which is inscribed the circle
                
        del draw # the drawing is done so no need to keep the draw object (from the official Pillow documentation example for ImageDraw)        


    ## Post-analysis methods ##
        
    def previous_step(self):
        """ 
        Asks for the display of the previous image step in the list. Slot method for the 'Previous step' button of the interface.
        
        :return: 0 if the step index exists, the non existing index otherwise
        :rtype: int
        
        .. codeauthor:: Laura Xénard
        """
        if self.project.analysis != None:
            newStep = (self.project.analysis.currentStep-1) % (len(self.project.analysis.steps) + 1)
            return self.go_to_step(newStep)
        
    def next_step(self):
        """ 
        Asks for the display of the next step image in the list. Slot method for the 'Next step' button of the interface.
        
        :return: 0 if the step index exists, the non existing index otherwise
        :rtype: int
        
        .. codeauthor:: Laura Xénard
        """
        if self.project.analysis != None:
            newStep = (self.project.analysis.currentStep+1) % (len(self.project.analysis.steps) + 1)
            return self.go_to_step(newStep)
                
    def go_to_step(self, iStep, radius=7, color='red'):
        """
        Updates the :class:`Analysis` information so that the UI module can display a new step image.
        Creates the image to display, with red spots to indicate the followex apex.
        Slot method for the display of a specific step from its index.
      
        :param int iStep: the index of the step to display
        :param int radius: the radius of the circle to draw
        :param str color: the color to use for the drawing
        :return: 0 if the step index exists, the non existing index otherwise
        :rtype: int
        :raise KeyError: if the specified key does not exist
        
        .. codeauthor:: Laura Xénard
        """
        
        if iStep == 0: # display of the final image
            self.project.analysis.stepImg = self.project.analysis.finalImg        
        
        else: # display of a step image
            try:
                apexCoord, imgIndex = self.project.analysis.steps[iStep]
                if isinstance(apexCoord, msh.Coordinates):
                    img = self.project.greyPics[imgIndex-1][0]
                    self.project.analysis.stepImg = img.copy() # copying the img so as to preserve the original img
                    
                    # Drawing a circle on the apex
                    draw = ImageDraw.Draw(self.project.analysis.stepImg)
                    draw.ellipse([(apexCoord.x-radius, apexCoord.y-radius), (apexCoord.x+radius, apexCoord.y+radius)], color) # coordinates of the square in which is inscribed the circle
                    del draw # the drawing is done so no need to keep the draw object (from the official Pillow documentation example for ImageDraw)                                
            
            except KeyError:
                print("WARNING! Inexisting key {}.".format(iStep))
                return(iStep) # return the inexisting key
            
        self.project.analysis.previousStepDisplayed = self.project.analysis.currentStep # update of the previously displayed step
        self.project.analysis.currentStep = iStep # update of the currently displayed step
        return 0 
    
    def colorImgNotDisplayed(self):
        self.project.analysis.currentStep = self.project.analysis.previousStepDisplayed    
        
    def clear(self):
        """
        Prepares the application for a new analysis.
        
        :return: a message indicating that the application is ready to run a new analysis
        :rtype: str
        
        .. codeauthor:: Laura Xénard
        """
        
        self.project.clear()
        return "Analysis deleted. The application is ready to run a new analysis on the previously loaded images."
    
    def close(self):
        """
        Deletes the :class:`Project` object to clear up the memory.
        
        :raise AttributeError: if no :class:`Project` instance exists
        
        .. codeauthor:: Laura Xénard
        """
        
        try:
            del self.project
        except AttributeError:
            print("INFORMATION: there's nothing to clear.")
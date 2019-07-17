# -*- coding: utf-8 -*-

#=============================================================================
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
    This module manages the inputs and the outputs of the system and sends the information received to the module :mod:`Management`.

.. moduleauthor:: Salomé Attar 
.. moduleauthor:: Laura Xénard
"""


import os
import operator
import datetime

import pickle
from PIL import Image, ImageDraw
import tifffile as tiff
import numpy as np

import Mushroom as msh


def new_directory(path): 
    """
    Creates a new directory thankes to the module :mod:`os`
    
    :param str path: the path to create the directory
    :raise IOError: if the specified directory has not been correctly created
    
    .. codeauthor:: Salomé Attar
    """
    
    try:
         os.mkdir(path)
    except IOError:
        return("An error occurred while creating the directory.")
   
def load_pictures(project): 
    """ 
    Loads the images from the directories 'skeletons' and 'regMosaic' given by the project path attribute.
    
    :param Project project: the project giving the path to the images to load
    :return: a tuple of a boolean and a string indicating the state of the creation of the project environment
    :rtype: (bool, str)
    :raise FileNotFoundError: if the skeleton or greyscale images directory has not been found
    :raise NotADirectoryError: if the path specified is not the path of a directory
    
    .. codeauthor:: Laura Xénard
    """
    
    # Filling of 'skelPics' with the skelettonized pictures to display
    skel_path = os.path.abspath(os.path.join(project.path + '/skeletons'))
    try:    
        with os.scandir(skel_path) as dirIt:
            for entry in dirIt:
                # If the item is an image file
                if entry.is_file() and is_img(entry.path):
                    img = Image.open(entry.path) # loading of the image (by pillow)
                    imgName = os.path.basename(entry.path) # name of the image
                    project.skelPics.append((img, imgName)) # add in the list                         
    except FileNotFoundError:
        return (False, "ERROR when loading skeletons: "
                     "directory not found.") 
    except NotADirectoryError:
        return (False, "ERROR when loading skeletons: "
                "the specified path does not match a directory.")    
    
    # Filling of 'grayPics' with the greyscale images to display
    grey_path = os.path.abspath(os.path.join(project.path + '/regMosaic'))
    try:    
        with os.scandir(grey_path) as dirIt:
            for entry in dirIt:
                # If the item is an image file
                if entry.is_file() and is_img(entry.path):
                    img = Image.open(entry.path) # loading of the image (by pillow)
                    img = img.convert('RGBA') 
                    imgName = os.path.basename(entry.path) # name of the iamge
                    project.greyPics.append((img, imgName)) # add in the list                          
    except FileNotFoundError:
        return (False, "ERROR when loading grayscale images: "
                     "directory not found.") 
    except NotADirectoryError:
        return (False, "ERROR when loading grayscale images: "
                "the specified path does not match a directory.")
 
    # Sorting lists to ensure that the images are in chronological order
    project.skelPics.sort(key = operator.itemgetter(1))
    project.greyPics.sort(key = operator.itemgetter(1))
    
    # Check of the length of the lists which gave to be the same
    if len(project.skelPics) != len(project.greyPics):
        return (False, "An error occured during the loading of the pictures:"
                "the number of skeletonized images and grayscale images are not the same")
    
    return(True, "Images successfully loaded.")
            
def new_environment(project):
    """
    Creates a new project environment:
        
        * load images from directories with absolute path 'path+skeletons' and 'path+regMosaic' thanks to the function :func:`load_pictures`;
        * if it doesn't exist, create a new directory 'save' in the path of the project; 
        * if it doesn't exist, create a new directory 'export' in the path of the project.
     
    :param Project project: the :class:`Project` whose environment needs to be created
    :return: a tuple of a boolean and a string indicating the state of the creation of the project environment
    :rtype: (bool, str)
        
    .. codeauthor:: Salomé Attar
    """
    
    # loading of the pictures
    loadingOK, message = load_pictures(project)
    if loadingOK:   
        # Directories to create
        save_path = os.path.abspath(os.path.join(project.path + '/save'))
        export_path = os.path.abspath(os.path.join(project.path + '/export'))
          
        # Creating of the directory 'save' and 'export' in the 'path'
        if os.path.exists(save_path) or os.path.exists(export_path):
            return (True, "The environment already exists.")
       
        new_directory(save_path) 
        new_directory(export_path)
        return (True, "The new environment was successfully created.")
    else:
        return (False, message)
           
def open_project(path_file):
    """
    Opens an already saved project.
   
    :param str path_file: the path to the project save
    :return: the :class:`Project` of the module :mod:`Mushroom` extracted from the save and a boolean and a string indicating the state of the creation of the project
    :rtype: (Project, bool, str)
    :raise FileNotFoundError: if no file can be found at the specified path
    :raise UnpicklingError: if the unpickling fails
    
    .. codeauthor:: Salomé Attar
    """
    
    try:
       with open(path_file,'rb') as file:
           
           try:
               my_depickler = pickle.Unpickler(file) #reading of the file
               project = my_depickler.load() #recording in the object
               loadingOK, message = load_pictures(project) # loading of the images (squelettons et greyscale)
               if loadingOK:
                   return (project, True, "Project loaded.")
               else:
                   return (project, False, message)
           except pickle.UnpicklingError:
                return (None, False, "Unpickling failed.")
        
    except FileNotFoundError:
        return (None, False, "No file has been found at the specified path.")
               
def save_project(project):
    """
    Saves the project in a file named by the date thanks to the module :mod:`datetime` without its images.
    
    :param Project project: the :class:`Project` to save
    :return: a message indicating if the saving worked
    :rtype: str
    :raise FileNotFoundError: if the save directory has not been found
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Salomé Attar
    """
    
    result = "Project saved."
    # copy of the pictures before delete them for the saving
    skelPicsCopy = project.skelPics.copy() 
    greyPicsCopy = project.greyPics.copy()
    
    # deleting of the pictures for the saving
    project.skelPics = [] 
    project.greyPics = []
    
    # put the name of the file in a format yyyy-mm-dd-hh-mm-ss (year,month,day,hour,minute,second)
    myDate = datetime.date.today()
    mytime = datetime.datetime.now()
    projetid = (str(myDate) + '-' + str(mytime.hour) + '-' + str(mytime.minute) + '-' + str(mytime.second))
    
    try:
        with open(os.path.abspath(os.path.join(project.path + '/save/ProjectNumber'+ projetid)), 'wb') as file:
            my_pickler = pickle.Pickler(file)
            my_pickler.dump(project)
    except FileNotFoundError:
        result = "An error occurred during the save. Directory not found."

    project.skelPics = skelPicsCopy.copy()
    project.greyPics = greyPicsCopy.copy()
    
    return result
                
def export_project(project, txtOk, imgOk, imgstepsOk):
    """
    Exports a project in a txt format and ask the user to enter comments if he needs to.
    The :class:`Project` is exported in a file named by the current date yyyy-mm-dd-hh-mm-ss.
   
    :param Project project: the :class:`Project` to export
    :param bool txtOk: a boolean indicating if the text data of the analysis should be exported
    :param bool imgOk: a boolean indicating if the final image of the analysis should be exported
    :param bool imgstepsOk: a boolean indicating if the list of the steps images should be exported
    :return: a message indicating if the project has been correctly exported
    :rtype: str
    :raise FileNotFoundError: if the save directory has not been found

    .. codeauthor:: Salomé Attar
    """
    
    result = "Analysis exported." 
    
    # creation of the file name
    myDate = datetime.date.today()
    mytime = datetime.datetime.now()
    projetid = (str(myDate) + '-' + str(mytime.hour) + '-' + str(mytime.minute) + '-' + str(mytime.second))
    
    # creation of the paths
    export_file_path = os.path.abspath(os.path.join(project.path + '/export/ProjectNumber' + projetid + '.txt'))
    export_img_path = os.path.abspath(os.path.join(project.path + '/export/ImageFinal' + projetid + '.tif'))
    export_steps_path = os.path.abspath(os.path.join(project.path + '/export/ImageSteps' + projetid + '.tif'))
    
    # if the analysis already exists
    if (os.path.exists(export_file_path)): 
            result = "This analysis have already been exported."
    else: # if its not the case and the user wants to export the text of the analysis
        try:
            if (txtOk == True):    
                with open (export_file_path,'w') as file:
                    file.write("Projet n. " + str(project.id))
                    file.write("\n")
                    file.write("\n")
                    file.write("* * Parametres de l'analyse * *") # parameters of the analysis : image of the start, image of the end and coordiantes of the apex selectionnated
                    file.write("\n")
                    file.write("Image de debut : " + str(project.greyPics[project.analysis.startImg][1]) + " (n. " + str(project.analysis.startImg + 1) + ")\n")
                    file.write("Image de fin : " + str(project.greyPics[project.analysis.endImg][1]) + " (n. " + str(project.analysis.endImg + 1) + ")\n")
                    file.write("Coordonnees de l'apex selectionne : " + str(project.analysis.startApex) + "\n")
                    
                    if project.notes != "":
                        file.write("Commentaires : " + str(project.notes) + "\n")
                    file.write("\n")
                    
                    file.write("* * Tableau des hyphes * *") # array of the hyphaes
                    file.write("\n")
                    i = 0
                    while i<len(project.analysis.hyphae): # for each hypha, its number and the list of the segments which composed it 
                        
                        file.write("N. hyphe |  Taille  | Segments qui la composent\n")
                        for key in project.analysis.hyphae:
                            value = project.analysis.hyphae[key]
                            hypha_line = "{:>8} |{:>9} | ".format(key, value[-1])
                            for seg in value[:-1]:
                                hypha_line += str(seg) + ", "
                            file.write(hypha_line + "\n")
                            i += 1
                                  
                    file.write("\n")
                    file.write("* * Tableau des segments * *") # array of the segments
                    file.write("\n")
                    i = 0
                    while i < len(project.analysis.segments):
                        file.write("N. segment |  Coordonnees debut  |   Coordonnees fin   |  Taille  | Evolution du segment => imgIndex: [apexCoord, taille]\n")
                        for key in project.analysis.segments.keys():
                            coord = project.analysis.segments[key].coord
                            size = project.analysis.segments[key].size
                            evo = project.analysis.segments[key].evolution                            
                            file.write("{:>10} |{:>20} |{:>20} | {:>8} | {}\n".format(key, str(coord[0]), str(coord[1]), size, evo))
                            i += 1
                            
                    file.close()
            
            if (imgOk == True):
                project.analysis.finalImg.save(export_img_path) # save of the analysis image
            
            if (imgstepsOk == True):
                with tiff.TiffWriter(export_steps_path) as stack:
                    export_steps(project, stack)

        except FileNotFoundError:
            result = "An error occurred during the export."
                
    return result

def is_img(path):
    """ 
    Checks that the file with the specified path 'path' is an image whose format is supported by the 'Image' class of PIL:
        
        * BMP 	Windows Bitmap
        * GIF 	Graphic Interchange Format (optional
        * JPG 	Joint Photographic Experts Group
        * JPEG 	Joint Photographic Experts Group
        * PNG 	Portable Network Graphics
        * PPM 	Portable Pixmap
        * TIFF 	Tagged Image File Format
        * XBM 	X11 Bitmap
    
    :param str path: the path of the file to check
    :return: True if the file that has been checked is in a supported format, False otherwise
    :rtype: bool
    
    .. codeauthor:: Laura Xénard
    """
    
    formats = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ppm', '.tif', '.tiff', '.xbm']
    fileFormat = os.path.splitext(path)[1] # extension of the file
    if fileFormat in formats:
        return True
    else:
        return False
    
def export_steps(project, stack, radius=7, color='red'):
        """
        Method that fills the colorPics attribute of :class:`Analysis` with the steps images in chronological order where the currently followed apex is represented by a red circle.
        
        :param int radius: radius of the circle to draw
        :param str color: color to use for the drawing
        
        .. codeauthor:: Laura Xénard
        """
        
        # For each step in chronological order
        for step, value in sorted(project.analysis.steps.items()):
            
            # Retrieving and copying of the image
            apexCoord = value[0] # 'Coordinates' of the followed apex for the step
            
            if isinstance(apexCoord, msh.Coordinates):
                indexImg = value[1]-1 # index of the greyscale image for the step
                img = project.greyPics[indexImg][0]
                imgColor = img.copy() # copying the img so as to preserve the original img
            
                # Drawing a circle on the apex
                draw = ImageDraw.Draw(imgColor)
                draw.ellipse([(apexCoord.x-radius, apexCoord.y-radius), (apexCoord.x+radius, apexCoord.y+radius)], color) # coordinates of the square in which is inscribed the circle
                del draw # the drawing is done so no need to keep the draw object (from the official Pillow documentation example for ImageDraw)
                
                npimg = np.asarray(imgColor)
                stack.save(npimg, compress=1) # compress : 0 = not compressed, 9 = very compressed
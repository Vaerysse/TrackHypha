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
    This module represents and manages the structure of the mycelium extracted from a data set throught these 5 classes:
    
        * Coordinates
        * HyphaSegment
        * Analysis
        * Project 

.. moduleauthor:: Sébastien Maillos
.. moduleauthor:: Laura Xénard
"""


import itertools


class Coordinates:
    """ 
    Class representing the Cartesian coordinates of a point in the plane.
    
    :param int coordX: the point abscissa
    :param int coordY: the point ordinate
        
    .. codeauthor:: Laura Xénard
    """
    
    def __init__(self, coordX, coordY):
        """
        Class constructor.
        
        .. codeauthor:: Laura Xénard
        """
        
        self.x = coordX
        self.y = coordY
        
        
    def __repr__(self):
        """
        Magic method for displaying the coordinates as (x, y).
        
        :return: the string representation of a 'Coordinates' object
        :rtype: str
        
        .. codeauthor:: Laura Xénard
        """
        
        return "({}, {})".format(int(self.x), int(self.y))
    
    
    def __add__(self, coord):
        """
        Overload of the addition for 2 :class:`Coordinates` objects.
        
        :return: the :class:`Coordinates` sum of the 2 Coordinates
        :rtype: Coordinates
            
        .. codeauthor:: Laura Xénard
        """
        
        xresult = self.x + coord.x
        yresult = self.y + coord.y
        return Coordinates(xresult, yresult)
        
        
class HyphaSegment:
    """
    Class representing a hypha segment which is the section of the hypha comprised between two nodes or between a node and an apex.
        
    :param int id: the id of the segment
    :param int previous: the id of the previous segment
    :param bool deadEnd: True if the segment is the last one of the hypha, False otherwise
    :param coord: the start and end :class:`Coordinates` of the segment
    :type coord: list[Coordinates]
    :param evolution: a dictionary of the evolution steps of the segment, linking the relevant image with the segment apex :class:`Coordinates` and its length
    :type evolution: dict{int : [Coordinates, int]}  
    :param int size: size of the hypha segment in pixel 
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Laura Xénard
    """
    
    segmentCount = itertools.count(1) # we start at 1
    
    def __init__(self, previousID, start):
        self.id = next(HyphaSegment.segmentCount)
        self.previous = previousID
        self.deadEnd = False
        self.coord = [start]
        self.evolution = {}
        self.size = 1


class Analysis:
    """
    Class representing an analysis run on an image dataset in fonction of the user's parameters.
        
    :param int id: the id of the analysis
    :param Coordinates startApex: the :class:`Coordinates` of the apex chosen as the starting point of the analysis
    :param int startImg: the index of the start image of the analysis
    :param int endImg: the index of the end image of the analysis
    :param steps: a dictionary of the analysis steps, linking the step index with the :class:`Coordinates` of the followed apex and the index of the corresponding image
    :type steps: dict{int : [Coordinates, int]}
    :param Image finalImg: an image showing the hyphae that have been explored by the analysis
    :param Image stepImg: an image showing the position of the explored apex for the current step
    :param int currentStep: the step currently being displayed
    :param int previousStepDisplayed: the step previously being displayed
    :param segments: a list of all the :class:`HyphaSegment` created by the analysis
    :type segments: list[HyphaSegment]
    :param hyphae: a hyphae dictionary linkink each hypha with the id of its segments
    :type hyphae: dict{int : list[int]}
    :param list_pixels: a list of :class:`Coordinates` of the hyphae pixels
    :type list_pixels: list[Coordinates]
    :param int processingTime: the processing time of the analysis
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Laura Xénard
    """
    
    analysisCount = itertools.count(1) # we start at 1
    
    def __init__(self, startApex, startImg):
        """
        Class constructor.
        
        .. codeauthor:: Sébastien Maillos
        .. codeauthor:: Laura Xénard
        """
        
        self.id = next(Analysis.analysisCount)
        self.startApex = startApex
        self.startImg = startImg
        self.endImg = None
        self.steps = {}
        self.finalImg = None
        self.stepImg = None
        self.currentStep = 0
        self.previousStepDisplayed = 0
        self.segments = {}
        self.hyphae = None
        self.list_pixels = []
        self.processing_time = 0 


class Project:
    """
    Class holding the project data.
       
    :param int id: the id of the project
    :param str path: the path to the project environment (directory)
    :param skelPics: a sorted list of tuples (img, img name) of skeleton images to analyze
    :type skelPics: list[(Image, str)]
    :param greyPics: a sorted list of tuples (img, img name) of greyscale images to display in the UI
    :type greyPics: list[(Image, str)]
    :param int currentImg: the index of the image currently being displayed
    :param int previousImgDisplayed: the index of the image previously being displayed
    :param str notes: notes on the analysis (the notes will be exported)
    :param Analysis analysis: the :class:`Analysis` object holding the analysis data    
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Laura Xénard
    """
    
    projectCount = itertools.count() # we start at 1
    
    def __init__(self, path):
        """
        Class constructor.
        
        .. codeauthor:: Sébastien Maillos
        .. codeauthor:: Laura Xénard
        """
        
        self.id = next(Project.projectCount) 
        self.path = path
        self.skelPics = [] # list (Image, skelName)
        self.greyPics = [] # list (Image, greyName)
        self.currentImg = 0 # we initialize at the first image
        self.previousImgDisplayed = 0 
        self.notes = ""
        self.analysis = None # we wait for startImg, endImg and startApex

        
    def clear(self):
        """
        Reinitiating the project so that a new analysis can be run on the same set of images. 
        The notes written at the previous analysis are being kept but can be changed during the export.
        
        :raise AttributeError: if there is no attribute :attr:`Analysis` for the current :class:`Project`
        
        .. codeauthor:: Laura Xénard
        """

        try:
            if self.analysis != None:
                del self.analysis # we destroy the previous analysis
        except AttributeError:
            print("INFORMATION: no analysis attribute for this Project instance.")
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
    The module AI enables the analysis on a given set of data.
    It allows the following of the evolution of an apex and all its hyphae daughters,
    the cutting into segments, the size calculation of each segment and the composition of all the hyphae.
    It also saves the id number of the image and the coordinates of the followed apex during 
    each step in order to make it easier to visualize it on the user interface.

.. moduleauthor:: Salomé Attar
.. moduleauthor:: Bouthayna Haltout
.. moduleauthor:: Sébastien Maillos
"""


import math 
import Mushroom as msh 


def play_analysis(pictures, analysis):
    """ 
    Method enabling the analysis managing and extracting the list data of the received images.

    :param pictures: list of successive hyphae growth images
    :type pictures: list[Image, str]
    :param Analysis analysis: the attribute :class:`Analysis` of the project 
    :return: True when the analysis is done, False otherwise and a string indicating the state of the analysis
    :rtype: (bool, str)
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Salomé Attar
    .. codeauthor:: Bouthayna Haltout    
    """

    # initialization of the variables :
    analyze = True
    segment = msh.HyphaSegment(0, analysis.startApex)
    segment.evolution[analysis.startImg] = (analysis.startApex,1)
    nodes = [] # Will contain a list of each entry. List components : 1: image of where the node is, 2: coordinates of the node.
    num_picture = analysis.startImg
    coord_analyze = analysis.startApex
    previous_coord_analyze = analysis.startApex
    list_skelPics = pictures
    check_pixel_no_hypha = False
    init_list_pixels(analysis.list_pixels, list_skelPics[num_picture], analysis.startApex)
    
    num_step = 0
    while analyze == True: # As long as the analysis is ongoing.
        num_step+=1
        list_foreign_pixel = []
        result = None
        # This part is launched only when the analysis changes the image to continue the following of the apex.
        # (Not for the return on an image through a node nor an artefact, because the analysis of the area and the referal of the pixels not belonging to the hypha has already been done.)
        if check_pixel_no_hypha == True:
            #Looks in the area of the new image and localize the pixels not belonging to the hypha and update list_foreign_pixel.
            photography_zone_comparison(list_skelPics[num_picture-1], list_skelPics[num_picture], analysis.list_pixels,list_foreign_pixel, previous_coord_analyze)
            # If needed, rectify the analysis coordinates ( if they change on the new image ).
            result = check_apexCoord_newPic(list_skelPics[num_picture-1], list_skelPics[num_picture], analysis.list_pixels, coord_analyze)
            check_pixel_no_hypha = False
            if result[1] == None:
                result="No analysis"
            else:
                coord_analyze = result[1] 
        if result != "No analysis":
            result = picture_analyze(list_skelPics[num_picture], analysis.list_pixels, list_foreign_pixel, coord_analyze) #A couple (string,coordinates).           
            if result[0] == "Error, pixel list is void":
                return (result[0], False)

        if result[0] == "Apex" :
            segment.deadEnd = True
            segment.evolution[num_picture] = [result[1], result[4]]
            num_picture+=1
            previous_coord_analyze = result[1]
            coord_analyze = result[1]
            if result[1] == "o" or result[1] == "n" or result[1] == "e" or result[1] == "N":
                analysis.steps[num_step] = [None, None]
            else:
                analysis.steps[num_step] = [result[1], num_picture]
            check_pixel_no_hypha = True
            
            if num_picture > analysis.endImg: # If it's the last image.
                segment.coord.append(result[1])
                segment.evolution[num_picture] = [result[1], result[4]]
                segment.deadEnd = True
                segment.size=calculated_size(segment)
                analysis.segments[segment.id] = segment
                if not nodes:
                    break
                else: # If none of the above, but the analysis continue. 
                    segment = msh.HyphaSegment(nodes[-1][2], nodes[-1][1])#We put nodes instead of result[2] because we go backwards and we want the coordinates of the last node.
                    segment.evolution[num_picture] = [(nodes[-1][1]),1]
                    num_picture=nodes[-1][0] # We go to the last node of the list, and we take the first on the list. 
                    coord_analyze=nodes[-1][1]
                    del nodes[-1] # We delete the last node from the list to update it.
              
        elif result[0] == "Node": # If the found pixel is a node.
            segment.coord.append(result[1]) # Segment update. 
            segment.evolution[num_picture] = [result[1], result[4]]
            segment.deadEnd = False
            segment.size = calculated_size(segment)
            analysis.segments[segment.id] = segment
            if result[1] == "o" or result[1] == "n" or result[1] == "e" or result[1] == "N":
                analysis.steps[num_step] = [None, None]
            else:
                analysis.steps[num_step] = [result[1], num_picture]
            previous_id = segment.id
            segment = msh.HyphaSegment(previous_id, result[2])
            segment.evolution[num_picture] = [result[2], 1]
            nodes.append([num_picture, result[3], previous_id])
            coord_analyze = result[2]
        elif result[0] == "No analysis":
            analysis.steps[num_step] = [None, None]
            num_picture+=1
        else: # If it's an artefact.
            segment.coord.append(result[1])
            segment.evolution[num_picture] = [result[1], result[4]]
            segment.deadEnd = True
            segment.size=calculated_size(segment)
            analysis.segments[segment.id] = segment
            if result[1] == "o" or result[1] == "n" or result[1] == "e" or result[1] == "N":
                analysis.steps[num_step]=[None, None]
            else:
                analysis.steps[num_step] = [result[1], num_picture]
            if not nodes:
                break
            else:
                segment = msh.HyphaSegment(nodes[-1][2], nodes[-1][1])
                segment.evolution[num_picture] = [(nodes[-1][1]), 1]
                num_picture = nodes[-1][0] # We go to the last node on the list, and on this list we want the first node.
                coord_analyze = nodes[-1][1]
                del nodes[-1] # We delete the last node from the list to update it.

    result_hyphae = list_hypha_creation(analysis.segments) 
    if result_hyphae == "Error, segments dict is void":
        return (result_hyphae, False)
    else:
        analysis.hyphae = result_hyphae
        
    return ("Analysis ended.", True)
        
def list_hypha_creation(segments):
    """
    Method allowing the construction of a dictionary of hyphae, 
    containing all the numbers of the hyphae segments which make up each one of them.
    
    :param segments: a dictionnary of :class:`HyphaSegment` with their ID numbers as key 
    :type segments: dict{int : list[HyphaSegment]}    
    :return: a dictionary of a list of :class:`HyphaSegment` number IDs with the number of the corresponding hypha as key
    :rtype: dict{int : list[int]}
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Salomé Attar
    """
    
    if not segments: # If the sent pixel list is empty, the analysis is impossible. 
         return "Error, segments dict is void" 
        
    hyphae = {}
    h = 1
    for value in segments.values():
        if value.deadEnd:
            hypha = [value.id]
            seg = value
            i = 0
            size = 0
            while seg.previous != 0:
               seg = segments.get(seg.previous)
               hypha.append(seg.id)
               size+=seg.size
               i+=1
            hypha.append(size)
            hyphae["h"+str(h)] = hypha
            h+=1
    return hyphae
 
def picture_analyze(picture, list_pixels, list_foreign_pixel, coord):
    """
    Method that will analyze the received image to see the evolution of the apex and return a new set of data. 
    
    :param picture: image tuple (skeleton) to analyze and its name
    :type picture: list[Image, str]
    :param list_pixels: list of :class:`Coordinates` of the already found pixels
    :type list_pixels: list[Coordinates]
    :param list_foreign_pixel: known pixels :class:`Coordinates` list not linked to the hypha in the ongoing analysis 
    :type list_foreign_pixel: list[Coordinates]
    :param Coordinates coord: coordinates of the pixel to analyze
    :return: a tuple stating if what has been found is a node, an apex, or an artefact, and suitable :class:`Coordinates`
    :rtype: (str, Coordinates, Coordinates, Coordinates, int)
     
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Salomé Attar
    """
     
    if not list_pixels: # If the sent pixel list is empty, the analysis is impossible. 
         return ("Error, pixel list is void", None, None, None, None)    
    
    list_pixels_segment = []         
    # Start of the loop of the pixel by pixel analysis.
    while(True):
        liste_temp = check_point(picture, coord, 3) 
        liste_temp = delete_pixel_same(liste_temp, list_pixels)
        liste_temp = delete_pixel_same(liste_temp, list_foreign_pixel)
        # According to the remaining number of pixels in the temporary list, we send to play_analyze different informations.
        if not liste_temp: # If the temporary list is empty, this means that the last found pixel was an Apex.
            return ("Apex", list_pixels[-1], None, None, len(list_pixels_segment))
        elif len(liste_temp) == 1: # If the temporary list contains a pixel, that means that we have to start over on the new pixel found.
            list_pixels_segment.append(liste_temp[0])
            list_pixels.append(liste_temp[0])
            coord=liste_temp[0]
        elif len(liste_temp) == 2: # If the temporary list contains 2 pixels, that means that the hypha is splitting in two, and that we have a node at that spot. 
            list_pixels_segment.append(liste_temp[0])
            list_pixels.append(liste_temp[0])
            list_pixels.append(liste_temp[1])
            # returns the coordunates in order: 1-Pixel of end of hypha segment, 2-Pixel of start of hypha segment following to analyze, 3-Pixel of start of hypha segment upcoming to store in Nodes.
            return ("Node", list_pixels[-3], list_pixels[-2], list_pixels[-1], len(list_pixels_segment))
        else: # if the temporary list contains more than 2 pixels, that means that there is an artefact in that emplacement on the image.
            return ("Artefact", list_pixels[-1], None, None, len(list_pixels_segment))
                
def check_point(picture, coord, size):
    """
    Method that will analyze the pixels around the :class:`Coordinates` received in the parameters of the pixel of the image.
    The size of the matrix is defined in the parameters.
    Once the analysis is completed, the already found pixels list is updated and precises if the image analysis must go on or not.
    If the analysis is not continued, it precises if the pixel is an apex, a node or an artefact.
    
    :param picture: an image tuple (skeleton) to analyze and its name 
    :type picture: list[Image, str]
    :param Coordinates coord: :class:`Coordinates` of the pixel to analyze
    :param int size: size of the matrix  
    :return: a list of all the white pixels coordinates of the area
    :rtype: list[Coordinates]
     
    .. codeauthor:: Sébastien Maillos
    """
    
    liste_temp = [] # create a temporary list to store the coordinates of the white pixels found during the analysis.
    
    if size%2 == 0:
        x = (coord.x)-size/2 # coordinates x of the last pixel of the list.
        y = (coord.y)-size/2 # coordinates y of the last pixel of the list.
        sizeM = size+1 # if the size of the matrix is even, it's transformed in an uneven matrix.
    else:
        x = (coord.x)-(size-1)/2 # coordinates x of the last pixel of the list.
        y = (coord.y)-(size-1)/2 # coordinates y of the last pixel of the list. 
        sizeM = size
    
    i = 0
    while i < sizeM: # travels all the abscissae of the matrix.
        j = 0
        while j < sizeM: # travels all the ordinates of the matrix.
            if picture[0].getpixel((x+i, y+j)) == 255: # if a pixel is white, we add it to the temporary list sent.
                liste_temp.append(msh.Coordinates(x+i, y+j))
            j += 1
        i += 1
    return liste_temp

def check_apexCoord_newPic(picture1, picture2, list_pixels, coord):
    """
    Method that will check if the starting pixels of the analysis of the skeletonized image match the :class:`Coordinates` of the previous image.
    
    :param picture1: an image tuple (skeleton) of the first image to analyze and its name
    :type picture1: list[Image, str] 
    :param picture2: an image tuple (skeleton) of the second image to analyze and its name
    :type picture2: list[Image, str]
    :param list_pixels: already found pixels coordinates list 
    :type list_pixels: list[Coordinates]
    :param Coordinates coord: :class:`Coordinates` of the pixel to analyze     
    :return: a tuple that precises that the analysis can start, and the :class:`Coordinates` of start of the analysis
    :rtype: (str, Coordinates)
     
    .. codeauthor:: Sébastien Maillos
    """
    
    list_temp = check_point(picture2, coord,3)
    list_temp = delete_pixel_same(list_temp, list_pixels)
        
    # If the pixel is still on the new image
    # Only if one or zero are unknown, then we can launch the analysis (the 2 pixels that we need for the analysis are on the right position).
    # :class:`Coordinates`If 2 pixels or more are unknown, I launch the rewriting of the end of the hypha function on the new image.
    if picture2[0].getpixel((coord.x, coord.y)) == 255 :
        if len(list_temp) == 1 :
            return ("Start analyzing", coord)
        else:
            list_temp = check_point(picture2, coord, 3)
            list_temp = delete_pixel_same(list_temp, [coord])
            for ele1 in list_pixels:
                if ele1 != coord:
                    for ele2 in list_temp:
                        if three_pixels(ele1.x, ele2.x, 1) == True and three_pixels(ele1.y, ele2.y, 1) == True :
                            list_pixels.append(ele2)
                            return ("Start analyzing", coord)

            return shift_correction(picture1, picture2, list_pixels, coord)
    
    else:
        return shift_correction(picture1,picture2, list_pixels, coord)

def connect_pixelCoord_newPic(picture, liste_pixel, coord):
    """
    Method that will see in a certain distance around the received :class:`Coordinates`, to determine the 2
    pixels neighbors the closest to the received :class:`Coordinates`.
    Then it will reconstruct the "path of pixel" of this pixel couple, by substituting 
    the :class:`Coordinates` between the position of the pixel couple and the received :class:`Coordinates` in list_pixel.
   
    :param picture: an image tuple (skeleton) to analyze and its name
    :type picture: list[Image, str]
    :param list_pixels: already found pixels :class:`Coordinates` list  
    :type list_pixels: list[Coordinates]
    :param Coordinates coord: :class:`Coordinates` of the pixel to analyze 
    :return: a tuple that specifies that the analysis can start, and specifies the :class:`Coordinates` of start of the analysis
    :rtype: (str, Coordinates)
     
    .. codeauthor:: Sébastien Maillos
    """

    liste_temp = check_point(picture, coord, 21)
    
    # travels the two lists (temporary and received) and delete from the temporary list all the unknown pixels (in the received list).
    temp = []
    i = 0
    while i < len(liste_temp):
        for coordPx in liste_pixel:
            if (not liste_temp) == False:
                if (liste_temp[i].x == coordPx.x) and (liste_temp[i].y == coordPx.y):
                    temp.append(liste_temp[i])
        i += 1
    
    liste_temp = temp # liste_temp now contains all the known pixels of the matrix to analyze.
    
    if not liste_temp:
        return None
    else:   
        # retrieves the index where we find those coodinates where we were supposed to work on.
        coord_position_liste_pixel = liste_pixel.index(coord)
    
        temp = []
        # travels liste_temp and removes all the pixels of which the index in liste_pixel is over the pixel of reference(coord).
        position_liste_pixel1 = -1 # We initialize it to -1 which will retrun an error if the variable doesn't change. 
        position_liste_pixel2 = -1 # We initialize it to -1 which will retrun an error if the variable doesn't change.
        # We only keep the known pixels in liste_pixel that are lower (index) than the referencial pixel (coord)
        for px in liste_temp:
            if liste_temp.index(px)<coord_position_liste_pixel:
                temp.append(px)
    
        liste_temp = temp
        i = len(liste_temp)-1
        # Travels the list backwards to find the pixel couple the closest from coord that hasn't changed its coordinates between the two images.
        # Starts from the bottomof the list(highest index)
        while i >= 0:
            # We check that the first pixel in liste_pixel is also present in liste_temp.
            for ipx in range(len(liste_pixel)):
                if (not liste_temp) == False:
                    if (liste_temp[i].x == liste_pixel[ipx].x) and (liste_temp[i].y == liste_pixel[ipx].y):
                        position_liste_pixel1 = ipx
                        # We then check if the previous pixel in liste_pixel is present also in liste_temp.
            for ipx in range(len(liste_temp)):
                if (not liste_temp) == False:
                    if (liste_pixel[position_liste_pixel1-1].x == liste_temp[ipx].x) and (liste_pixel[position_liste_pixel1-1].y == liste_temp[ipx].y):
                        position_liste_pixel2 = position_liste_pixel1-1
            # If the two positions are known then at it's the end of the search, otherwise we try again.
            if (position_liste_pixel1 and position_liste_pixel2) != -1:
                break
            else:
                position_liste_pixel1 = -1
                position_liste_pixel2 = -1
                i-=1   

        # Phase of reconstruction in the liste_pixel between the found couple and coord.
        nbp = coord_position_liste_pixel-position_liste_pixel1
        false_liste = [liste_pixel[position_liste_pixel2], liste_pixel[position_liste_pixel1]]
        i = 0
        while i < nbp:
            result = check_point(picture, false_liste[i+1], 3)
            result = delete_pixel_same(result, false_liste)  
            if len(result) == 1:
                liste_pixel[position_liste_pixel1+i+1] = result[0]
                false_liste.append(result[0])
                coord = liste_pixel[position_liste_pixel1+i+1]
            else:
                break
            i += 1
    
        return ("Start analyzing", coord)

def delete_pixel_same(list1, list2):
    """
    Method that will remove from list1 all the pixels :class:`Coordinates` from list2.
    
    :param list1: pixels list
    :type list1: list[Coordinates]
    :param list2: pixels list
    :type list2: list[Coordinates]
    :return: a list of all the :class:`Coordinates` of unknown pixels in list2
    :rtype: list[Coordinates] 
    
    .. codeauthor:: Sébastien Maillos
    """
    
    i = 0
    while i < len(list1):
        stop = False
        for coordPx in list2:
            if (not list1) == False and stop == False and list1[i].x == coordPx.x and list1[i].y == coordPx.y:
                del list1[i]
                stop = True # Avoid list2 of being once again traveled.
                i -= 1
        i += 1
    return list1

def photography_zone_comparison(picture1, picture2, list_pixels, list_foreign_pixel, coord):
    """
    Method that "captures" an area of 120 pixel of radius around a point (coord) on an image, then checks all the pixels that don't belong to the analyzed hypha.
    Then, it "captures" the same area on a new image to tell where the pixels that don't belong to the currently analysed hypha are located (and adds them to list_foreign_pixel).
    
    :param picture1: an image tuple (skeleton) of the first image to analyze and its name
    :type picture1: list[Image, str] 
    :param picture2: an image tuple (skeleton) of the second image to analyze and its name
    :type picture2: list[Image, str]
    :param list_pixels: already found pixels :class:`Coordinates` list 
    :type list_pixels: list[Coordinates]
    :param list_foreign_pixel:  :class:`Coordinates` list of a known pixel that don't belong to the currently analyzed hypha
    :type list_foreign_pixel: list[Coordinates]
    :param Coordinates coord: :class:`Coordinates` of the pixel to analyze  
    
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Salomé Attar
    """
    
    # check the white pixels in a radius of 120 around the coord on the previous image.
    list_temp = check_point(picture1, coord, 201)
    # Delete from the list all the pixels are known from the hypha.
    list_temp = delete_pixel_same(list_temp, list_pixels)
    # Delete from the list all the known pixels that don't belong to the hypha.
    # list_temp=delete_pixel_same(list_temp,list_foreign_pixel)
    
    # Add the found pixels to list_foreign_pixel.
    if len(list_temp) > 0:
        for ele in list_temp:
            list_foreign_pixel.append(ele)
        # Check all the white pixels on the new image.
        list_temp = check_point(picture2, coord, 201)
    
        # Copy list_foreign_pixel to travel it and be able to modify it without having to impact the loop "for".
        copy_list_foreign_pixel = []
        for ele in list_foreign_pixel:
            copy_list_foreign_pixel.append(ele)
        
        for ele1 in list_temp:
            for ele2 in copy_list_foreign_pixel:
                # Check if from those pixels there is some at a (max) 3 pixel radius of distance.
                if three_pixels(ele1.x, ele2.x, 3) == True and three_pixels(ele1.y, ele2.y, 3) == True:
                    # Then we add them to list_foreign_pixel
                    list_foreign_pixel.append(ele1)

def three_pixels(x1, x2, ray):
    """
    Method that compares 2 numbers to see if there's a gap of 3 or less between them.
    
    :param int x1: a number to compare
    :param int x2: a number to compare  
    :param int ray: a size of distance to comppare
    :return: True if less than 3 of gap, False otherwise
    :rtype: bool
    
    .. codeauthor:: Sébastien Maillos
    """

    if x1-x2 < (ray+1) and x1-x2 > -(ray+1):
        return True
    else:
        return False
    
def shift_correction(picture1, picture2, list_pixels, coord):
    """
    Method that allows the rectification of the localisation of the last pixels on the next analyzed image throughout a lag.
    
    :param picture1: an image tuple (skeleton) of the first to analyze and it's name
    :type picture1: list[Image, str] 
    :param picture2: an image tuple (skeleton) of the second to analyze and it's name
    :type picture2: list[Image, str]
    :param list_pixels: coordinates list of an already found pixel
    :type list_pixels: list[Coordinates]
    :param Coordinates coord: coordinates of the pixel to analyze
    :return: a message stating the start of the analysis, along with the rectified coordinates of start of the analysis 
    :rtype: (str, Coordinates)
   
    .. codeauthor:: Sébastien Maillos
    .. codeauthor:: Bouthayna Haltout
    """

    ray = 5
    resultat1 = check_point(picture1 ,coord, ray)
    resultat2 = check_point(picture2, coord, ray)
    if len(resultat2) < 5:
        ray = 7
        resultat1 = check_point(picture1, coord, ray)
        resultat2 = check_point(picture2, coord, ray)
        if len(resultat2) < 5:
            ray = 9
            resultat1 = check_point(picture1, coord, ray) # We check all the pixels on a radius of 4 around the coord on picture 1 (11 = 5*2 +1)
            resultat2 = check_point(picture2, coord, ray) # We check all the pixels on a radius of 4 around the coord on picture 2
         
    nb_pixels = len(resultat1)-1 # It will be the number of pixels to replace on list_pixels.
    
    if nb_pixels > 0 and len(list_pixels) > nb_pixels:
        px_bord = list_pixels[-nb_pixels] # We want the pixel on the edge of the on checkpoint area.
    else:
       return ("Error shift_correction", None)

    px_start = None
    for ele in resultat2:
        if three_pixels(ele.x, px_bord.x, 1) == True and three_pixels(ele.y, px_bord.y, 1) == True:
            px_start = ele
            break
    if px_start == None:
        for ele in resultat2:
            if three_pixels(ele.x, px_bord.x, 2) == True and three_pixels(ele.y, px_bord.y, 2) == True:
                px_start=ele
                break
    if px_start == None:
        for ele in resultat2:
            if three_pixels(ele.x, px_bord.x, 3) == True and three_pixels(ele.y, px_bord.y, 3) == True:
                px_start = ele
                break

    if px_start == None:
        return ("Not a pixel", None)

    list_px3 = check_point(picture2, px_start, ray)
    ele_ok = 0
    for ele in list_px3:
        list_temp = check_point(picture2, ele, 3)
        list_temp = delete_pixel_same(list_temp, resultat2)
        if len(list_temp) == 2:
            list_pixels[-(nb_pixels+1)] = ele
            ele_ok += 1
        elif len(list_temp) == 1:
            list_pixels[-nb_pixels] = ele
            ele_ok += 1
        if ele_ok == 2:
            break
    i = nb_pixels-1
    list_temp2 = []
    while i > 0:
        list_temp = check_point(picture2, list_pixels[-(i+1)], 3)
        list_temp = delete_pixel_same(list_temp, list_pixels)  
        if len(list_temp) >= 1:
            list_pixels[-i] = list_temp[0]
            list_temp2.append(list_temp[0])
        else:
            list_pixels[-i] = list_pixels[-(i+1)]
            list_pixels[-(i+1)] = list_pixels[-(i+2)]
        if list_pixels[-i] == list_pixels[-1]:
            break
        i -= 1 
    
    i = 0
    while i < 3:
        list_temp = check_point(picture2, list_pixels[-1], 3)
        list_temp = delete_pixel_same(list_temp, list_temp2)
        if len(list_temp) == 1:
            list_temp2.append(list_temp[0])
            list_pixels.append(list_temp[0])
            i += 1
        else:
            break
            
    return ("Start analyzing", list_pixels[-1])
        
def init_list_pixels(list_pixels, picture, coord):    
    """
    Method that initializes list_pixel by filling it with the 7 pixels of end that follow the selected apex.
    
    :param list_pixel: a pixel list
    :type list_pixel: list[Coordinates]
    :param picture1: an image tuple (skeleton) to analyze and its name
    :type picture1: list[Image, str]
    :param Coordinates coord: :class:`Coordinates` of a white pixel 
    
    .. codeauthor:: Sébastien Maillos
    """
    
    # We look in a radius of 10 around the selected point.
    list_temp = check_point(picture, coord, 21)
    
    for px in list_temp:
        if len(check_point(picture, px, 3)) == 2:
            coord = px
            i = 0
            while i < 8:
                list_pixels.append(px)
                i += 1
            i = 0
            while i < 7:
                list_pixel_temp = check_point(picture, list_pixels[-(1+i)], 3)
                list_pixel_temp = delete_pixel_same(list_pixel_temp, list_pixels)
                list_pixels[-(2+i)] = list_pixel_temp[0]
                i += 1
            break

def is_apex(picture, coord):
    """
    Method that determines if the selected :class:`Coordinates` are those of an apex. 
    
    :param picture1: an image tuple (skeleton) of the first image to analyze and its name
    :type picture1: list[Image, str]
    :param Coordinates coord: :class:`Coordinates` of a pixel  
    :return: a boolean precising if there is an apex on the selected point, and the real point of the apex. 
    :rtype: (bool, str)
    
    .. codeauthor:: Sébastien Maillos
    """
    
    # We check in a radius of 10 around the selected point.
    list_temp = check_point(picture, coord, 21)
    
    # If the list is empty, no white pixel so no apex.
    if not list_temp:
        return (False, None)
    # Otherwise, we travel list_temp and look in a radius of 1 for each point. 
    # If there is only 2 white pixels, then we know that it is an apex for sure and we return its coordinates to start the analysis. 
    else:
        for px in list_temp:
            if len(check_point(picture, px, 3)) == 2:
                return (True, px)
    return (False, None)

def calculated_size(segment):
    """
     Method that calculates the size of a :class:`HyphaSegment` (itself containing several :class:`HyphaSegment`).
     
     :param HyphaSegment segment: one HyphaSegment     
     :return: the size of the segment (in pixels)
     :rtype: int
     
     .. codeauthor:: Sébastien Maillos
     """
    
    if not segment:
        return "Error, the segment is void"
    
    size = 0
    for ele in segment.evolution.values():
        if ele[1] == "n" or ele[1] == None:
            size += 0
        else:
            size += ele[1]
    return size
    
def apex_path_verification(coord1, segment):
     """
     Method that defines whether the apex identified on the image matches the trajectory of the apex on the previous image.
     
     :param Coordinates coord: :class:`Coordinates` of the followed apex
     :param HyphaSegment segment: the last :class:`HyphaSegment` saved     
     :return: a boolean indicating if this is the right apex that was followed
     :rtype: bool
     
     .. codeauthor:: Salomé Attar
     """
     
     # The model of evolution of the hyphae being imprivisible I consider that it is indeed the same apex if it is 'not far' from the vector.
     # Which mean in a triangle that revolves around the vector.
     
     # A vector is composed of two points.
     # I consider my vector as the segment shift from itself.
     vect_pt1 = segment.coord[0]+ msh.Coordinates(1,0)
     vect_pt2 = segment.coord[1]
        
     # In an arbitrary way I consider that the apex of the current image corresponds to the apex followed.
     # if it's in the triangle, more or less 1/4 away from the Vector.
     x = coord1.coordX
     y = coord1.coordY
   
     return ((x <= math.fabs(vect_pt2.coordX - vect_pt1.coordX))and(y<= math.fabs((vect_pt2.coordY*1.25) - vect_pt1.coordY)))
       


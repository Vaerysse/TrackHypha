# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 14:04:19 2019
Updated on Thu Mar 14 17:26:00 2019

Module de tests unitaires pour le module Mushroom.

@author: laura
"""

import unittest

import Mushroom as msh


class MushroomTest(unittest.TestCase):
      
    def test_add_coord(self):
        """
        Teste l'addition de deux Coordinates. 
        
        @author: laura
        """
        
        self.coord1 = msh.Coordinates(3, 5)
        self.coord2 = msh.Coordinates(-3, 0)
        self.coord3 = self.coord1 + self.coord2
        self.assertEqual(self.coord1.x + self.coord2.x, self.coord3.x)
        self.assertEqual(self.coord1.y + self.coord2.y, self.coord3.y)
        self.assertIsInstance(self.coord3, msh.Coordinates)
        
        

        
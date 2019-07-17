# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:51:35 2019
Updated on Thu Mar 14 16:10:00 2019

Module of tests  for the module InOut.

..moduleauthor:: Salomé, Laura

"""

import os
import shutil
import unittest
import Mushroom as msh
import InOut


class InOutTest(unittest.TestCase):    
    
    def setUp(self):
        """ 
        Initialization. 
        
        ..codeauthor:: Laura Xénard
        """

        # For the is_img tests
        self.path_img = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/InOut_test_is_img/")
        
        # For the new_environment tests
        path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_new_environment/")
        self.project_test_new_environment = msh.Project(path)
 
    
    def test_is_img_with_dir(self):
        """
        Tests is_img() with a directory.
        
        ..codeauthor:: Laura Xénard
        """
        
        self.assertFalse(InOut.is_img(self.path_img + "dossier_vide"))
        
    def test_is_img_with_file_not_img(self):
        """
        Tests is_img() with a file a file that is not an image.
        
        ..codeauthor:: Laura Xénard
        """        
        
        self.assertFalse(InOut.is_img(self.path_img + "blabla.txt"))
                
    def test_is_img_with_jpg(self):
        """
        Tests is_img() with a jpg image.
        
        ..codeauthor:: Laura Xénard
        """
   
        self.assertTrue(InOut.is_img(self.path_img + "Logo_Paris_Diderot.jpg"))
               
    def test_is_img_with_png(self):
        """
        Tests is_img() with a png image.
        
        ..codeauthor:: Laura Xénard
        """
                   
        self.assertTrue(InOut.is_img(self.path_img + "Logo_Paris_Descartes.png"))
                
    def test_is_img_with_tif(self):
        """
        Tests is_img() with a jpg tif.
        
        ..codeauthor:: Laura Xénard
        """
                   
        self.assertTrue(InOut.is_img(self.path_img + "mycelium.tif"))     
        
    def test_new_environment_1_good(self):
        """
        Test if the creation of a new environment works when everything is ok.
        Result expected: yes.
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """    
       
        self.assertEqual(InOut.new_environment(self.project_test_new_environment), (True, "The new environment was successfully created."))         
        
    def test_new_environment_2_already_existing(self):
        """
        Test if an already existing environment can be created again.
        Result expected: yes.
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        self.assertEqual(InOut.new_environment(self.project_test_new_environment), (True, "The environment already exists."))
        
        # Cleaning after the test
        path = os.path.abspath(os.path.join(self.project_test_new_environment.path + '/save'))
        shutil.rmtree(path, ignore_errors=True)
        path = os.path.abspath(os.path.join(self.project_test_new_environment.path + '/export'))
        shutil.rmtree(path, ignore_errors=True)

    def test_save_project_good(self):
        """
        Test if an existing project (whose environment was created) can be saved.
        Result expected : yes
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_success/")
        project_save_success = msh.Project(path)
        self.assertEqual(InOut.save_project(project_save_success), "Project saved.")
        
        # Cleaning after the test
        path = os.path.abspath(os.path.join(project_save_success.path + '/save/'))
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)
                   
    def test_save_project_null(self):
        """
        Test if a project can be saved if the environment doesn't exist.
        Result expected : no.
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_fail/")
        project_save_fail = msh.Project(path)
        self.assertEqual(InOut.save_project(project_save_fail), "An error occurred during the save. Directory not found.")
  
    def test_open_project_good(self):
        """
        Test if a project already saved can be open.
        Result expected: yes.
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        path_open_success = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_open/save/test_save_open")
        self.assertEqual(InOut.open_project(path_open_success)[1:], (True, "Project loaded."))
        
    def test_open_project_no_directory(self):
        """
        Test if a project not saved can be open.
        Result expected : no.
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        path_open_fail = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_fail/save/test_save")
        self.assertEqual(InOut.open_project(path_open_fail)[1:], (False, "No file has been found at the specified path."))
        
    def test_export_project(self):
        """
        Test if a created project can be exported.
        Result expected : yes
        
        ..codeauthor:: Salomé Attar, Laura Xénard
        """
        
        # If everything goes well
        path_export_success = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_open/save/test_save_open")
        project1 = InOut.open_project(path_export_success)[0]
        self.assertEqual(InOut.export_project(project1, True, False, False), "Analysis exported.")
        
        # Cleaning after the test
        path = os.path.abspath(os.path.join(project1.path + '/export/'))
        shutil.rmtree(path, ignore_errors=True)
        
        # If the export directory does not exist
        path_export_fail = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + "/Ressources_pour_tests_unitaires/Project_test_export_fail/save/test_save_export")
        project2 = InOut.open_project(path_export_fail)[0]
        self.assertEqual(InOut.export_project(project2, True, False, False), "An error occurred during the export.")
        
        # Cleaning after the test
        os.mkdir(path)
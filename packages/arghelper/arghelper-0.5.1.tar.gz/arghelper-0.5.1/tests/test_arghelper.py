# -*- coding: utf-8 -*-
# Copyright (c) 2014-2016 The arghelper developers. All rights reserved.
# Project site: https://github.com/questrail/arghelper
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for arghelper.py.
"""
import argparse
import os
import unittest
import arghelper


class TestExtantItem(unittest.TestCase):

    def setUp(self):  # NOQA
        self.existing_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'existing_dir')

        self.non_existing_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'non_existing_dir')

        self.existing_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'existing_file.txt')

        self.non_existing_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'non_existing_file.txt')

    def test_extant_item_directory_exists(self):
        """Test that a directory exists"""
        self.assertEqual(
            arghelper.extant_item(self.existing_dir, "directory"),
            self.existing_dir)

    def test_extant_item_directory_does_not_exist(self):
        """Test that a non-existing directory doesn't exist"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_item,
            self.non_existing_dir,
            "directory")

    def test_extant_item_directory_not_file(self):
        """Test that an existing file doesn't exist as a directory"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_item,
            self.existing_file,
            "directory")

    def test_extant_item_file_exists(self):
        """Test that a file exists"""
        self.assertEqual(
            arghelper.extant_item(self.existing_file, "file"),
            self.existing_file)

    def test_extant_item_file_does_not_exist(self):
        """Test that a non-existing file doesn't exist"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_item,
            self.non_existing_file,
            "file")

    def test_extant_item_file_not_directory(self):
        """Test that an existing directory doesn't exist as a file"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_item,
            self.existing_dir,
            "file")


class TestExtantDirectory(TestExtantItem):

    def test_extant_directory_exists(self):
        """Test that a directory exists"""
        self.assertEqual(
            arghelper.extant_dir(self.existing_dir),
            self.existing_dir)

    def test_extant_directory_does_not_exist(self):
        """Test that a non-existing directory doesn't exist"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_dir,
            self.non_existing_dir)

    def test_extant_directory_not_file(self):
        """Test that an existing file doesn't exist as a directory"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_dir,
            self.existing_file)


class TestExtantFile(TestExtantItem):

    def test_extant_file_exists(self):
        """Test that a file exists"""
        self.assertEqual(
            arghelper.extant_file(self.existing_file),
            self.existing_file)

    def test_extant_file_does_not_exist(self):
        """Test that a non-existing file doesn't exist"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_file,
            self.non_existing_file)

    def test_extant_file_not_directory(self):
        """Test that an existing directory doesn't exist as a file"""
        self.assertRaises(
            argparse.ArgumentError,
            arghelper.extant_file,
            self.existing_dir)


class TestParseConfigInputOutput(unittest.TestCase):

    def setUp(self):  # NOQA
        self.script_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'sample.py')
        self.config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'config_file.csv')
        self.input_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'input_dir')
        self.output_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'output_dir')
        self.argv = [self.script_name,
                     self.config_file,
                     self.input_dir,
                     self.output_dir]

    def test_parse_config_input_output(self):
        """Test the parse_config_input_output function"""
        args = arghelper.parse_config_input_output(self.argv)
        self.assertEqual(args.config_file,
                         self.config_file)
        self.assertEqual(args.input_dir,
                         self.input_dir)
        self.assertEqual(args.output_dir,
                         self.output_dir)


class TestParseConfig(unittest.TestCase):

    def setUp(self):  # NOQA
        self.script_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'sample.py')
        self.config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'config_file.csv')
        self.argv = [self.script_name,
                     self.config_file]

    def test_parse_config(self):
        """Test the parse_config function"""
        args = arghelper.parse_config(self.argv)
        self.assertEqual(args.config_file,
                         self.config_file)


if __name__ == '__main__':
    unittest.main()

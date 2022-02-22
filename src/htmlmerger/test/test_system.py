import os
import unittest

from htmlmerger.main_generic.main import generic_main

class TestBasicCases(unittest.TestCase):

  def test_run_main(self):
    #setup
    #run
    generic_main ()
    #check
    # (error check is done automatically)
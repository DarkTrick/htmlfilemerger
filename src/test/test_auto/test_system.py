import os
import tempfile
import unittest
import sys
import tempfile

from htmlmerger.htmlmerger.main import main

class TestBasicCases(unittest.TestCase):
  _TEST_ROOT_DIR = "./test/testfiles"

  #def test_run_main(self):
    #setup
    #run
    #main ()
    #check
    # (error check is done automatically)


#  def test_process_file(self):
#    #setup
#    infile = os.path.join (self._TEST_ROOT_DIR, "basic_1","testfile.html")
#    infile = os.path.abspath (infile)
#    outfile = tempfile.mktemp ()
#    sys.argv = [1,infile, outfile]
#    #run
#    main ()
#    #check
#    # todo
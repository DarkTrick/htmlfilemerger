
import os
import sys
from .htmlmerger import HtmlMerger
from .myutils import *

gHelp = """
Merge JS/CSS/images/HTML into one single file
Version: 1.0

Usage:
  htmlmerger inputfile [optional: outputfile]

"""



def merge(strInfile, strOutfile):

  if (not os.path.isfile (strInfile)):
    print ("FATAL ERROR: file `" + strInfile + "` could not be accessed.")
    return

  baseDir = os.path.split (os.path.abspath (strInfile))[0]

  #read file
  content = getFileContent (strInfile)

  parser = HtmlMerger()
  content_changed = parser.run (content, baseDir)

  # log errors
  if (len (parser.messages) > 0):
    print ("Problems occured")
    for msg in parser.messages:
      print ("  " + msg)
    print ("")

  # debug:
  if (False):
    print (content_changed)
    exit ()


  # write result
  with open (strOutfile, "w") as file:
    file.write (content_changed)



def mainfunc():
  args = sys.argv[1:] # cut away pythonfile
  if (len (args) < 1):
    print (gHelp)
    exit()

  inputFile = args[0]

  # get output file name
  outputFile = ""
  if (True):
    outputFile = os.path.splitext (inputFile)[0] + "_merged.html"

    if (len (args) > 1):
      outputFile = args[1]

    if (os.path.isfile (outputFile)):
      print ("FATAL ERROR: Output file " + outputFile + " does already exist")
      exit ()

  # run the actual merge
  merge (inputFile, outputFile)


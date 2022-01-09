from html.parser import HTMLParser
import os
import sys


gHelp = """
Merge JS/HTML into one single file
TODO: also merge CSS
      also merge images

Usage:
  htmlmerger.py inputfile [optional: outputfile]

"""


def getFileContent (strFilepath):
  content = ""
  with open (strFilepath, "r") as file:
    content = file.read ()
  return content


class HtmlMerger(HTMLParser):
  """
    Call "run(htmlContent, basedir)"  to merge
    script/css/images referenced withing htmlContent
    into one single html file.
  """
  def __init__(self):
    super().__init__()
    self._result = ""
    self._additionalData = ""
    self._baseDir = ""
    self.messages = []



  def _addMessage_fileNotFound(self, file_asInHtmlFile, file_searchpath):
    self.messages.push ("Error: Line " + self.getpos () +
                        ": Could not find file `" + file_asInHtmlFile +
                        "`; searched in `" + file_searchpath + "`." )



  def handle_starttag(self, tag, attrs):
      self._result += "<" + tag + " "

      for attr in attrs:
        key = attr[0]
        value = attr[1]

        # main work: read source content and add it to the file
        if (tag == "script" and key == "src"):
          #self._result += "type='text/javascript'"
          strReferencedFile = os.path.join (self._baseDir, value)
          if (not os.path.isfile (strReferencedFile)):
            self._addMessage_fileNotFound (value, strReferencedFile)
            continue
          referencedContent = getFileContent (strReferencedFile)
          self._additionalData += referencedContent

          # do not process this key
          continue

        # TODO: merge CSS
        # TODO: merge images


        # choose the right quotes
        if ('"' in value):
          self._result += key + "='" + value + "' "
        else:
          self._result += key + '="' + value + '" '

      self._result +=  ">"

  def _writeAndResetAdditionalData(self):
    self._result += self._additionalData
    self._additionalData = ""

  def handle_endtag(self, tag):
    self._writeAndResetAdditionalData ()
    self._result += "</" + tag + ">"


  def handle_data(self, data):
    self._result += data

  def run(self, content, basedir):
    self._baseDir = basedir
    self.feed (content)
    return self._result



def merge(strInfile, strOutfile):

  if (not os.path.isfile (strInfile)):
    print ("FATAL ERROR: file `" + strInfile + "` could not be accessed.")
    return

  baseDir = os.path.split (os.path.abspath (strInfile))[0]

  #read file
  content = getFileContent (strInfile)

  parser = HtmlMerger()
  content_changed = parser.run (content, baseDir)
  #print (content_changed)


  # write result
  with open (strOutfile, "w") as file:
    file.write (content_changed)


def main():
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


main()
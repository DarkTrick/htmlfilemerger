from html.parser import HTMLParser
import os
import sys
import base64


gHelp = """
Merge JS/CSS/images/HTML into one single file
Version: 1.0

Usage:
  htmlmerger inputfile [optional: outputfile]

"""


def getFileContent (strFilepath):
  content = ""
  with open (strFilepath, "r") as file:
    content = file.read ()
  return content



def getFileContentBytes (strFilepath):
  content = b""
  with open (strFilepath, "rb") as file:
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
    self.messages.append ("Error: Line " + str (self.getpos ()[0]) +
                        ": Could not find file `" + str (file_asInHtmlFile) +
                        "`; searched in `" + str (file_searchpath) + "`." )



  def _getAttribute (self, attributes, attributeName):
    """Return attribute value or `None`, if not existend"""
    for attr in attributes:
      key = attr[0]
      if (key == attributeName):
        return attr[1]
    return None


  def _getFullFilepath (self, relPath):
    return os.path.join (self._baseDir, relPath)


  def handle_starttag(self, tag, attrs):

    # Style references are within `link` tags. So we have to
    #  convert the whole tag
    if (tag == "link"):
      href = self._getAttribute (attrs, "href")
      if (href):
        hrefFullPath = self._getFullFilepath (href)
        if (not os.path.isfile (hrefFullPath)):
          self._addMessage_fileNotFound (href, hrefFullPath)
          return
        styleContent = getFileContent (hrefFullPath)
        self._result += "<style>" + styleContent + "</style>"
        return

    self._result += "<" + tag + " "

    for attr in attrs:
      key = attr[0]
      value = attr[1]

      # main work: read source content and add it to the file
      if (tag == "script" and key == "src"):
        #self._result += "type='text/javascript'"
        strReferencedFile = self._getFullFilepath (value)
        if (not os.path.isfile (strReferencedFile)):
          self._addMessage_fileNotFound (value, strReferencedFile)
          continue
        referencedContent = getFileContent (strReferencedFile)
        self._additionalData += referencedContent

        # do not process this key
        continue

      if (tag == "img" and key == "src"):
        imgPathRel = value
        imgPathFull = self._getFullFilepath (imgPathRel)
        if (not os.path.isfile (imgPathFull)):
          self._addMessage_fileNotFound (imgPathRel, imgPathFull)
          continue

        imageExtension = os.path.splitext (imgPathRel)[1][1:]
        imageFormat = imageExtension

        # convert image data into browser-undertandable src value
        image_bytes = getFileContentBytes (imgPathFull)
        image_base64 = base64.b64encode (image_bytes)
        src_content = "data:image/{};base64, {}".format(imageFormat,image_base64.decode('ascii'))
        self._result += "src='" + src_content + "'"

        continue



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
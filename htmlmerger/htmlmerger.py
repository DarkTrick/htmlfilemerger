from html.parser import HTMLParser
import base64
from myutils import *
import os

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




  def _getFullFilepath (self, relPath):
    return os.path.join (self._baseDir, relPath)

  def _getEncodedImageContent (self, imgRelPath_nullable):
    """
    Return: success: The encoded content of an image (that browsers understand)
            fail: None
    """
    if (None == imgRelPath_nullable):
      return None
    imgPathRel = imgRelPath_nullable

    imgPathFull = self._getFullFilepath (imgPathRel)
    if (not os.path.isfile (imgPathFull)):
      self._addMessage_fileNotFound (imgPathRel, imgPathFull)
      return None

    imageExtension = os.path.splitext (imgPathRel)[1][1:]
    imageFormat = imageExtension

    # convert image data into browser-undertandable src value
    image_bytes = getFileContentBytes (imgPathFull)
    image_base64 = base64.b64encode (image_bytes)
    encodedData = "data:image/{};base64, {}".format(imageFormat,image_base64.decode('ascii'))

    return encodedData



  def _keyValueToString(self, key, value):
    quote = "'"

    # change quotes if necessary
    if (quote in value):
      quote = '"'

    return " " + key + "=" + quote + value + quote



  def _tagToString (self, tag: str, dictAttributes):
    result = "<" + tag

    for key in dictAttributes:
      val = dictAttributes[key]
      result += self._keyValueToString (key, val)

    result += ">"

    return result


  def _writeAndResetAdditionalData(self):
    self._result += self._additionalData
    self._additionalData = ""

  def handle_endtag(self, tag):
    self._writeAndResetAdditionalData ()
    self._result += "</" + tag + ">"


  def handle_data(self, data):
    self._result += data


  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)

    # --------------------------------------------------
    # --  Main work: replace stuff, that's referenced --
    # --------------------------------------------------
    if (tag == "link"):
      rel = dict_getSafe (attrs, "rel")
      if (rel == "stylesheet"):
        href = dict_getSafe (attrs, "href")
        if (href):
          hrefFullPath = self._getFullFilepath (href)
          if (not os.path.isfile (hrefFullPath)):
            self._addMessage_fileNotFound (href, hrefFullPath)
            return
          styleContent = getFileContent (hrefFullPath)
          self._result += "<style>" + styleContent + "</style>"
          return

      if (rel == "icon"):
        href = dict_getSafe (attrs, "href")
        href = self._getEncodedImageContent (href)

        attrs["href"] = href
        self._result += self._tagToString (tag, attrs)
        return


    if (tag == "img"):
      src = dict_getSafe (attrs, "src")
      src = self._getEncodedImageContent (src)

      attrs["src"] = src
      self._result += self._tagToString (tag, attrs)
      return

    if (tag == "script"):
      src = dict_getSafe (attrs, "src")
      strReferencedFile = self._getFullFilepath (src)
      if (not os.path.isfile (strReferencedFile)):
        self._addMessage_fileNotFound (src, strReferencedFile)
        return
      referencedContent = getFileContent (strReferencedFile)
      self._additionalData += referencedContent

      dict_removeSafe (attrs, "src")
      self._result += self._tagToString (tag, attrs)
      return


    # --------------------------------------------------
    # --  Nothing to process; Just copy/paste content --
    # --------------------------------------------------
    self._result += self._tagToString (tag, attrs)



  def run(self, content: str, basedir: str):
    self._baseDir = basedir
    self.feed (content)
    return self._result
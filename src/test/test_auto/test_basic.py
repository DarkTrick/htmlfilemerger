import unittest
import os
from htmlmerger.htmlmerger.htmlmerger import HtmlMerger


class TestBasicCases(unittest.TestCase):
  _TEST_ROOT_DIR = "./test/test_auto/testfiles"

  def test_testdir_exists(self):
    self.assertTrue(os.path.isdir(self._TEST_ROOT_DIR), "Test-files directory is not accessible. Check the path!")

  def test_justHtmlTag(self):
    # setup
    subject = HtmlMerger ()

    # run
    actual = subject.run ("<html></html>", "./")

    # test
    self.assertEqual (actual, "<html></html>")


  def TODOtest_javascriptFile(self):
    # setup
    subject = HtmlMerger ()
    input = "<html><head>" + \
            "  <script type='text/javascript'  src='./javascriptfile.js'></script>" + \
            "</head></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <script type='text/javascript'>var foo = 0;</script>" + \
               "</head></html>"
    self.assertEqual (actual, expected)



  def test_cssFile(self):
    # setup
    subject = HtmlMerger ()
    input = "<html><head>" + \
            "  <link type='text/css' href='cssfile.css' rel='stylesheet'>" + \
            "</head></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <style>.myclass{font: 100;}</style>" + \
               "</head></html>"
    self.assertEqual (actual, expected)



  def test_imagePng(self):
    # setup
    subject = HtmlMerger ()
    input = "<html><body>" + \
            "  <img src='img.png'>" + \
            "</body></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)
    # test
    expected = '<html><body>' + \
               '  <img src=\'data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAYAAAABCAYAAAD9yd/wAAAACXBIWXMAAArEAAAKxAFmbYLUAAAAGklEQVQImS3CsQ0AAAzDIJ/ez8lSQYoLPYoBr/IOcyqJfFwAAAAASUVORK5CYII=\'>' + \
               '</body></html>'
    self.assertEqual (actual, expected)



  def test_link_icon(self):
    # setup
    self.maxDiff = None
    subject = HtmlMerger ()
    input = "<html><head>" + \
            "  <link type='image/vnd.microsoft.icon' href='icon.ico' rel='icon'>" + \
            "</head></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <link type='image/vnd.microsoft.icon' href='data:image/ico;base64, AAABAAEAEBACAAEAAQCwAAAAFgAAACgAAAAQAAAAIAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAAoisAAK6rAACiJwAAv/8AAP//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' rel='icon'>" + \
               "</head></html>"
    self.assertEqual (actual, expected)



  def test_javascriptFile_not_existing(self):
    """Test behavior if file does not exist"""
    # setup
    subject = HtmlMerger ()
    input = "<html><head>" + \
            '  <script async="" src="./non_existing_file.js"></script>' + \
            "</head></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <script>/* file ./non_existing_file.js not found */</script>" + \
               "</head></html>"
    self.assertEqual (actual, expected)



  def test_script_urilist(self):
    """Test behavior for  `<script id="x" type="text/uri-list">`"""

    # setup
    subject = HtmlMerger ()
    input = "<html><head>" + \
            '  <script id="x" type="text/uri-list">https://a.com</script>' + \
            "</head></html>"

    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <script id='x' type='text/uri-list'>https://a.com</script>" + \
               "</head></html>"
    self.assertEqual (actual, expected)





  def test_encodedPath(self):
    # setup
    targetFile = "javascript%20file%20with%20spaces.js"
    subject = HtmlMerger ()
    input = "<html><head>" + \
            "  <script type='text/javascript'  src='./" + targetFile + "'></script>" + \
            "</head></html>"


    # run
    actual = subject.run (input, self._TEST_ROOT_DIR)

    # test
    expected = "<html><head>" + \
               "  <script type='text/javascript'>var foo = 0;</script>" + \
               "</head></html>"
    self.assertEqual (actual, expected)






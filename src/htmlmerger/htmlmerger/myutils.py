
from typing import Union


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

def dict_getSafe(dict, key):
  """Return:
      key exists: value of dictionary
      else:       None
  """
  if (not key in dict):
    return None
  return dict[key]

def dict_removeSafe(dict, key):
  """Tries to remove `key`. If there is no `key`, ignore"""
  if (not key in dict):
    return None
  return dict.pop (key)
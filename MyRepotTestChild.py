"""

"""

import Ares#

# No Child for this page
CHILD_PAGES = {
  'test2': 'MyRepotTestChild2'
}

def report(aresObj, localPath=None):
  """
  """
  aresObj.title(1, 'I am a child')
  aresObj.anchor('Great link to a new page, again !', 'test2', CHILD_PAGES, localPath)
  return aresObj.html(localPath, title='Second Page')
	
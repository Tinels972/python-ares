""" Report Interface

This module will be used to produce the final report
It will link the HTML generation with the Javascript and Graphs parts

Users will be able to create bespoke reports from this wrapper using the standard HTML functions from the
module LibReportHTML. There is no need in this section to write HTML string, this class will only struture the
component and allow users to change them.

Any new HTML component should be written in the module LibReportHtml.py

The Report Class will contain only information about formatting in order to produce the final String
report in the function html()

In Ares there is no Javascript and CSS module integrated.
Basically as long as your version of Jquery, NVD3 and D3 are recent enought to support the fragments of HTML and
javascript defined in the different classes. It is possible to test the different features in the AresWrapper module.

QUESTION: Should we call the html() function in the wrapper or should we let the user call it ?
"""
# TODO: To use it to replace the redondant functions calls
# TODO: implement a decorator to wrap the current part in the functions

import inspect
import AresHtml
import AresGraph

htmlFactory = None # This is the factory with all the alias and HTML classes
# the below global variables are only used locally to generate the secondary pages and Ajax calls
LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES = None, None, None, None

def mapHtmlItems():
  """ Map the aliases to the HTML objects """
  htmlObjs = {}
  for name, obj in inspect.getmembers(AresHtml):
    if inspect.isclass(obj) and obj.alias is not None:
      htmlObjs[obj.alias] = obj
  return htmlObjs

def htmlLocalHeader(directory, report, statisPath, cssFiles, javascriptFiles):
  """ Add the header to the report when we are producing a text file - namely local run """
  global LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES

  LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES = directory, statisPath, cssFiles, javascriptFiles
  htmlFile = open(r"%s\%s.html" % (directory, report), "w")
  htmlFile.write('<!DOCTYPE html>\n')
  htmlFile.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr"> \n')
  htmlFile.write('<head>\n')
  htmlFile.write('%s<meta charset="utf-8">\n' % AresHtml.INDENT)
  htmlFile.write('%s<meta http-equiv="X-UA-Compatible" content="IE=edge">\n' % AresHtml.INDENT)
  htmlFile.write('%s<meta name="viewport" content="width=device-width, initial-scale=1">\n' % AresHtml.INDENT)
  htmlFile.write('%s<title>Local HTML Report</title>\n' % AresHtml.INDENT)
  for style in cssFiles:
    htmlFile.write('%s<link rel="stylesheet" href="%scss/%s" type="text/css">\n' % (AresHtml.INDENT, statisPath, style))
  for javascript in javascriptFiles:
    htmlFile.write('%s<script src="%sjs/%s"></script>\n' % (AresHtml.INDENT, statisPath, javascript))
  htmlFile.write('</head>\n')
  htmlFile.write('<body><div class="container">\n\n')

  return htmlFile

def htmlLocalFooter(htmlFile):
  """ Close all the HTML report and close the input text File - namely locally """
  htmlFile.write('\n</div>\n</body>\n')
  htmlFile.write('</html>\n')
  htmlFile.close()

class Report(object):
  """
  Ares Interface

  Main module to link the user reports and the HTML and Graph modules.

  """

  def __init__(self):
    """
    """
    global htmlFactory

    # Internal variable that should not be used directly
    # Those variable will drive the report generation
    self.__countItems = 0
    self.__content, self.__jsGraph, self.navTitle = [], [], []
    self.__htmlItems, self.jsOnLoad = {}, {}
    if htmlFactory is None:
      htmlFactory = mapHtmlItems()
    #for name, htmlCls in htmlFactory.items():
    #  print(name)

  def container(self):
    """
    """

  def structure(self):
    return self.content

  def item(self, itemId):
    """ Return the HTML object """
    return self.__htmlItems[itemId]

  def div(self, value):
    """

    Return the object ID to help on getting the object back. In any time during the
    report generation. THis ID is not supposed to change and it will be the
    """
    htmlObject = AresHtml.Div(self.__countItems, value)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def list(self, values):
    """ """
    htmlObject = AresHtml.List(self.__countItems, values)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def table(self, cols, values):
    """ """
    htmlObject = AresHtml.Table(self.__countItems, cols, values)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def dropDown(self, title, values):
    """ """
    htmlObject = AresHtml.DropDown(self.__countItems, title, values)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def dropZone(self):
    """ """
    htmlObject = AresHtml.DropZone(self.__countItems)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def textArea(self):
    """ """
    htmlObject = AresHtml.TextArea(self.__countItems)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def select(self, values):
    """ """
    htmlObject = AresHtml.Select(self.__countItems, values)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def container(self, htmlObj):
    """ """
    del self.__content[self.__content.index(htmlObj.htmlId)] # Is not defined in the root structure
    htmlObject = AresHtml.Container(self.__countItems, htmlObj)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def grid(self, htmlObjLeft, htmlObjRight):
    """ """
    del self.__content[self.__content.index(htmlObjLeft.htmlId)] # Is not defined in the root structure
    del self.__content[self.__content.index(htmlObjRight.htmlId)] # Is not defined in the root structure

    htmlObject = AresHtml.Split(self.__countItems, htmlObjLeft, htmlObjRight)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def button(self, value, cssCls=None):
    htmlObject = AresHtml.Button(self.__countItems, value, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def input(self, name, value):
    """ """
    htmlObject = AresHtml.Input(self.__countItems, name, value)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def text(self, value, cssCls=None):
    """ """
    htmlObject = AresHtml.Text(self.__countItems, value, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def code(self, value, cssCls=None):
    """ """
    htmlObject = AresHtml.Code(self.__countItems, value, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def paragraph(self, value, textObjsList=None, cssCls=None):
    """ """
    if textObjsList is not None:
      for textObj in textObjsList:
        del self.__content[self.__content.index(textObj.htmlId)] # Is not defined in the root structure

    htmlObject = AresHtml.Paragraph(self.__countItems, value, textObjsList, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def title(self, dim, value, cssCls=None):
    """ """
    htmlObject = AresHtml.Title(self.__countItems, dim, value, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    self.navTitle.append(htmlObject)
    return htmlObject.htmlId

  def pieChart(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    graphContainer = AresHtml.Graph(self.__countItems, width, height, cssCls=cssCls)
    self.__htmlItems[graphContainer.htmlId] = graphContainer
    self.__content.append(graphContainer.htmlId)
    self.__countItems += 1

    graphObject = AresGraph.Donut(graphContainer.htmlId, values)
    self.__jsGraph.append(graphObject)
    return graphContainer.htmlId

  def cloudChart(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    graphContainer = AresHtml.Graph(self.__countItems, width, height, cssCls=cssCls)
    self.__htmlItems[graphContainer.htmlId] = graphContainer
    self.__content.append(graphContainer.htmlId)
    self.__countItems += 1

    graphObject = AresGraph.WordCloud(graphContainer.htmlId, values)
    self.__jsGraph.append(graphObject)
    return graphContainer.htmlId

  def tree(self, cols, values, width=960, height=500, cssCls=None):
    """ """
    graphContainer = AresHtml.Graph(self.__countItems, width, height, withSgv=False, cssCls=cssCls)
    self.__htmlItems[graphContainer.htmlId] = graphContainer
    self.__content.append(graphContainer.htmlId)
    self.__countItems += 1

    graphObject = AresGraph.IndentedTree(graphContainer.htmlId, cols, values)
    self.__jsGraph.append(graphObject)
    return graphContainer.htmlId

  def comboLineBar(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    graphContainer = AresHtml.Graph(self.__countItems, width, height, cssCls=cssCls)
    self.__htmlItems[graphContainer.htmlId] = graphContainer
    self.__content.append(graphContainer.htmlId)
    self.__countItems += 1

    graphObject = AresGraph.ComboLineBar(graphContainer.htmlId, values)
    self.__jsGraph.append(graphObject)
    return graphContainer.htmlId

  def anchor(self, value, link, structure, localPath, cssCls=None):
    """ Add an anchor HTML tag to the report """
    if localPath is not None:
      # There is a child and we need to produce the sub Report attached to it
      #
      childReport = structure[link].replace(".py", "")
      htmlPage = htmlLocalHeader(LOCAL_DIRECTORY, childReport, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES)
      htmlPage.write(__import__(childReport).report(Report(), localPath=LOCAL_DIRECTORY))
      htmlLocalFooter(htmlPage)

      link = "%s.html" % childReport
    htmlObject = AresHtml.A(self.__countItems, value, link, cssCls=cssCls)
    self.__htmlItems[htmlObject.htmlId] = htmlObject
    self.__content.append(htmlObject.htmlId)
    self.__countItems += 1
    return htmlObject.htmlId

  def html(self, localPath, title=None, menu=True):
    """ Main function used to generate the report

    """
    # TODO: add the menu
    results, jsResults = [], []

    results.append('<script>')
    for jsOnLoad in self.jsOnLoad.keys():
      results.append(jsOnLoad)
    results.append('</script>')

    if menu:
      results.append('<div class="page-wrapper">')
      results.append('%s<div class="doc-wrapper">' % AresHtml.INDENT)
      results.append('%s%s<div class="container">' % (AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s<div class="doc-body">' % (AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s<div class="doc-sidebar hidden-xs">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s%s<nav id="doc-nav">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s%s%s<ul id="doc-menu" class="nav doc-menu" data-apy="affix">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      for section in self.navTitle:
        #subItems = self.navBar[section]
        results.append('<li><a href="%s">%s</a></li>' % (section.htmlId, section.val))
        #if subItems:
        #  jsResults.append('<ul class="nav doc-sub-menu">')
        #  for subItems in subItems:
        #    jsResults.append('<li><a href="%s">%s</a></li>')
        #  jsResults.append('</ul>')
      results.append("</ul></nav></div>")
    if title is not None:
      titleObj = AresHtml.Title(self.__countItems, 1, title)
      results.append(titleObj.html())
    results.append('</div></div></div></div>')

    for htmlId in self.__content:
      results.append(self.__htmlItems[htmlId].html())
      if self.__htmlItems[htmlId].jsEvent is not None:
        for fnc, fncDef in self.__htmlItems[htmlId].jsEvent:
          if fnc in ['drop', 'dragover']:
            jsResults.append('%s.bind("%s", function (event){' % (self.__htmlItems[htmlId].jsRef(), fnc))
            jsResults.append(fncDef)
            jsResults.append('});\n')
          else:
            jsResults.append('%s.%s(function(){' % (self.__htmlItems[htmlId].jsRef(), fnc))
            jsResults.append(fncDef)
            jsResults.append('});\n')

    if self.__jsGraph:
      jsResults.append("nv.addGraph(function() {\n")
      for jsgraphs in self.__jsGraph:
        jsResults.append(jsgraphs.js(localPath))
        jsResults.append("\n\n")
      jsResults.append("});\n")

    # Section dedicated to write all the extra Javascript callback functions
    # This will allow the page to be interactive
    results.append("<script>")
    results.extend(jsResults)
    results.append("</script>\n")
    return "\n".join(results)

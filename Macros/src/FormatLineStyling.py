import os
import fileinput
import xml.dom.minidom

DIRECTORY = '/Users/gargi/P4P_Output/Test/'
TEMP_FILE_NAME = "temp.svg"

ALL_SVGS = [];

for root, dirs, files in os.walk(DIRECTORY):
    for file in files:
        if file.endswith("Orthographic.svg"):
             ALL_SVGS.append(os.path.join(root, file))

for filename in ALL_SVGS:
  temp = open(DIRECTORY + TEMP_FILE_NAME, "w")
  doc = xml.dom.minidom.parse(filename)
  tagname = doc.getElementsByTagName('g')
  for t in tagname:
    if 'stroke' in t.attributes.keys():
      if (t.attributes['stroke'].value=="#000000"):
        t.setAttribute('stroke-width', "20")
        print("Changed solid line width")
      if 'stroke-dasharray' in t.attributes.keys():
        if (t.attributes['stroke'].value=="#ff0000"):
          t.setAttribute('stroke-dasharray', "60,30,20,30")
          print("Changed centreline spacing")
        if (t.attributes['stroke'].value=="#afafaf"):
          t.setAttribute('stroke-dasharray', "60,60")
          print("Changed hidden line spacing")
  temp.write(doc.toprettyxml())
  temp.close()
  os.rename(DIRECTORY + TEMP_FILE_NAME, filename)
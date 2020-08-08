import os
import fileinput
import xml.dom.minidom

DIRECTORY = '/Users/gargi/P4P_Output/Test/' # Directory to recursively search for SVG files in
TEMP_FILE_NAME = "temp.svg"
ALL_SVGS = [];

print("Finding SVGs to modify.")

for root, dirs, files in os.walk(DIRECTORY):
    for file in files:
        if file.endswith("Orthographic.svg"):
             ALL_SVGS.append(os.path.join(root, file)) # Adding all SVGs in the specified directory and nested directories

print("Found " + str(len(ALL_SVGS)) + " to modify.")

print("Making modifications...")

for filename in ALL_SVGS:
  temp = open(DIRECTORY + TEMP_FILE_NAME, "w") # Opening a temp file to write to
  doc = xml.dom.minidom.parse(filename)
  tagname = doc.getElementsByTagName('g')
  for t in tagname:
    if 'stroke' in t.attributes.keys(): # Modifying line styling information
      if (t.attributes['stroke'].value=="#000000"):
        t.setAttribute('stroke-width', "20")
      if 'stroke-dasharray' in t.attributes.keys():
        if (t.attributes['stroke'].value=="#ff0000"):
          t.setAttribute('stroke-dasharray', "60,30,20,30")
        if (t.attributes['stroke'].value=="#afafaf"):
          t.setAttribute('stroke-dasharray', "60,60")
  temp.write(doc.toprettyxml()) # Writing new SVG to temp
  temp.close()
  os.rename(DIRECTORY + TEMP_FILE_NAME, filename) # Renaming temp to the original filename

print("Modifications completed!")